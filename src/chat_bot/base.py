from typing import List

from langchain.agents import Tool
from langchain.chat_models.base import BaseChatModel
from langchain.memory.chat_memory import BaseChatMemory


class ChatBotBase():
    llm: BaseChatModel = None
    memory: BaseChatMemory = None
    tools: List[Tool] = []

    def __init__(self):
        pass

    def load_memory():
        pass

    def ask(self, message: str) -> str:
        response = self.agent_chain.run(message)
        return response

    @classmethod
    def get_messages_from_memory(cls, memory: BaseChatMemory) -> List[List[str]]:
        messages = []

        history = memory.load_memory_variables(messages)['history']
        for message in history:
            messages.append([message.type, message.content])

        return messages
