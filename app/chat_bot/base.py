import os
from typing import List

from langchain.agents import Tool, AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_memory import BaseChatMemory

from repository import message_history
from models import MessageType


class ChatBotBase:
    llm: BaseChatModel = None
    memory: BaseChatMemory = None
    agent_chain: AgentExecutor = None
    tools: List[Tool] = []

    def __init__(self, debug: bool = False):
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=10,
            return_messages=True,
        )
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            request_timeout=os.environ["OPENAI_REQUEST_TIMEOUT"],
            temperature=0,
        )
        self.agent_chain = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=debug,
            memory=self.memory,
            handle_parsing_errors=True,
            max_execution_time=os.getenv("MAX_EXECUTION_TIME"),
        )

    def load_memory(self, user_email: str):
        self.memory.clear()

        messages = message_history.get_last_k_messages(user_email, k=10)
        for message in messages:
            if message.message_type == MessageType.HUMAN.value:
                self.memory.chat_memory.add_user_message(message.content)
            elif message.message_type == MessageType.AI.value:
                self.memory.chat_memory.add_ai_message(message.content)

    async def ask(self, user_email: str, message: str) -> str:
        message_history.add_message(
           user_email, message, MessageType.HUMAN.value
        )
        response = await self.agent_chain.arun(message)
        message_history.add_message(
            user_email, response, MessageType.AI.value
        )

        return response
