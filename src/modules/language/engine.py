from langchain import HuggingFaceHub, LLMChain
from langchain.agents import load_tools
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
# from langchain.tools import BraveSearch
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationKGMemory, ConversationSummaryBufferMemory, CombinedMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.callbacks.manager import CallbackManager

from .tools import search_news, weather_forecast, generate_write_tool, python_repl
from .agents import ConversationalAgent
from .logger import Logger

class LanguageEngine:

    def __init__(self):
        self.temperature = 0
        self.setup_agents()
        self.tools = []
        self.memory = []
        self.callback_manager = None

    def setup_tools(self):
        tools = load_tools([
            "arxiv",
            "wikipedia",
            "wolfram-alpha",
            "ddg-search",
        ])
        tools = tools + [
            search_news,
            weather_forecast,
            python_repl,
            # BraveSearch.from_api_key(api_key="BSAEz8Y72g-9ou6IGATP-J-R02J0d1v", search_kwargs={"count": 3}),
            generate_write_tool(self),
        ]
        self.tools = tools

    def setup_memory(self):
        model = "tiiuae/falcon-7b-instruct"
        # used to summarize old convos and extract KG 
        llm = HuggingFaceHub(repo_id=model, model_kwargs={"temperature":0.8, "max_length": 100})
        db_store = SQLChatMessageHistory(connection_string='sqlite:///tmp/messages.db', session_id='chatbot')
        conversation_memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", input_key="input", chat_memory=db_store)
        self.kg_memory = ConversationKGMemory(llm=llm, input_key="input")
        # We can't use KG and entity_memory at the same time (why?)
        # entity_memory = ConversationEntityMemory(llm=OpenAI(), input_key="input", entity_store=EntitySqliteMemory(session_id="chatbot"))
        self.memory = CombinedMemory(memories=[conversation_memory, self.kg_memory])

    def setup_callback_manager(self):
        manager = CallbackManager.configure(verbose=True)
        manager.add_handler(Logger(), False)
        self.callback_manager = manager

    def setup_agents(self):
        self.setup_tools()
        self.setup_memory()
        self.setup_callback_manager()

        # https://blog.langchain.dev/plan-and-execute-agents/
        # self.planner = load_chat_planner(llm)
        # self.executor = load_agent_executor(llm, tools, verbose=True)
        # self.agent = PlanAndExecute(planner=self.planner, executor=self.executor, memory=self.memory, verbose=True)
        model = "tiiuae/falcon-7b"
        llm = HuggingFaceHub(repo_id=model, model_kwargs={"temperature":0.8, "max_length": 100})
        self.agent = AgentExecutor.from_agent_and_tools(
            agent=ConversationalAgent.from_llm_and_tools(
                llm,
                tools=self.tools,
                memory=self.memory,
                verbose=True
            ),
            tools=self.tools,
            callback_manager=self.callback_manager,
            memory=self.memory,
            verbose=True
        )

    def remember(self, user_input, output="okay"):
        self.kg_memory.save_context({"input": user_input}, {"output": output})

    def answer_question(self, text):
        response = self.agent.run(text)
        # Not sure if this is really necessary
        self.remember(text, response)
        # May be better to do this async on a cronjob
        self.kg_memory.kg.write_to_gml('tmp/knowledge_graph.gml')
        return (response)
