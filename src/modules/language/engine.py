import os, sys
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationKGMemory, ConversationSummaryBufferMemory, CombinedMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from .tools import search_news, weather_forecast, generate_write_tool

class LanguageEngine:

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.temperature = 0
        self.tools = []
        if (api_key is None):
            raise Exception("OPENAI_API_KEY not found in environment variables")
        self.setup_agent()

    def setup_agent(self):
        llm = OpenAI(temperature=self.temperature)
        tools = load_tools(self.tools)
        tools = tools + [search_news, weather_forecast, generate_write_tool(self)]
        db_store = SQLChatMessageHistory(connection_string='sqlite:///messages.db', session_id='chatbot')
        conversation_memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", input_key="input", chat_memory=db_store)
        self.kg_memory = ConversationKGMemory(llm=llm, input_key="input")
        # KG memory is better
        # entity_memory = ConversationEntityMemory(llm=OpenAI(), input_key="input", entity_store=EntitySqliteMemory(session_id="chatbot"))
        self.memory = CombinedMemory(memories=[conversation_memory, self.kg_memory])
        self.agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=self.memory, verbose=False)

    def remember(self, text):
        self.kg_memory.save_context({"input": text}, {"output": "okay"})

    def answer_question(self, text):
        response = self.agent.run(text)
        # May be better to do this async on a cronjob
        self.kg_memory.kg.write_to_gml('knowledge_graph.gml')
        return (response)
