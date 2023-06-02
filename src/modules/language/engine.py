import os, sys
from langchain import HuggingFaceHub, LLMChain
from langchain.agents import load_tools, initialize_agent
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
# from langchain.tools import BraveSearch
from langchain.llms import OpenAI
from langchain.memory import ConversationKGMemory, ConversationSummaryBufferMemory, CombinedMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from .tools import search_news, weather_forecast, generate_write_tool, python_repl

class LanguageEngine:

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.temperature = 0
        self.tools = [
            "arxiv",
            "wikipedia",
            "wolfram-alpha",
            "ddg-search",
        ]
        if (api_key is None):
            raise Exception("OPENAI_API_KEY not found in environment variables")
        self.setup_agents()

    def setup_agents(self):
        # llm = OpenAI(temperature=self.temperature)
        llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b", model_kwargs={"temperature":0.1})
        tools = load_tools(self.tools)
        tools = tools + [
            search_news,
            weather_forecast,
            python_repl,
            # BraveSearch.from_api_key(api_key="BSAEz8Y72g-9ou6IGATP-J-R02J0d1v", search_kwargs={"count": 3}),
            generate_write_tool(self),
        ]
        db_store = SQLChatMessageHistory(connection_string='sqlite:///messages.db', session_id='chatbot')
        conversation_memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", input_key="input", chat_memory=db_store)
        self.kg_memory = ConversationKGMemory(llm=llm, input_key="input")
        # KG memory is better ?
        # entity_memory = ConversationEntityMemory(llm=OpenAI(), input_key="input", entity_store=EntitySqliteMemory(session_id="chatbot"))
        self.memory = CombinedMemory(memories=[conversation_memory, self.kg_memory])
        # self.planner = load_chat_planner(llm)
        # self.executor = load_agent_executor(llm, tools, verbose=True)
        # https://blog.langchain.dev/plan-and-execute-agents/
        #self.agent = PlanAndExecute(planner=self.planner, executor=self.executor, memory=self.memory, verbose=True)
        self.agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=self.memory, verbose=True)

    def remember(self, user_input, output="okay"):
        self.kg_memory.save_context({"input": user_input}, {"output": output})

    def answer_question(self, text):
        response = self.agent.run(text)
        # Not sure if this is really necessary
        self.remember(text, response)
        # May be better to do this async on a cronjob
        self.kg_memory.kg.write_to_gml('knowledge_graph.gml')
        return (response)
