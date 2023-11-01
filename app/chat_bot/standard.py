import os
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import AgentType, initialize_agent
from langchain.utilities import GoogleSearchAPIWrapper

from .base import ChatBotBase


class ChatBotStandard(ChatBotBase):
    def __init__(
        self, open_ai_model_name="gpt-3.5-turbo", number_stored_messages=10, debug=False
    ):
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=number_stored_messages,
            return_messages=True,
        )

        self.llm = ChatOpenAI(
            model_name=open_ai_model_name,
            openai_api_key=os.environ["OPENAI_API_KEY"],
            request_timeout=120,
            temperature=0,
        )

        search = GoogleSearchAPIWrapper()
        self.tools = [
            Tool(
                name="Google Search",
                description="Search Google for recent results.",
                func=search.run,
            )
        ]

        self.agent_chain = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=debug,
            memory=self.memory,
            handle_parsing_errors=True,
        )

    def load_memory(self):
        pass

    def ask(self, message: str) -> str:
        response = self.agent_chain.run(message)
        return response
