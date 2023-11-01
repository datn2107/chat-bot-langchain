from .base import ChatBotBase
from .free import ChatBotFree
from .standard import ChatBotStandard

class ChatBotFactory:
    free_chatbot = ChatBotFree()
    standard_chatbot = ChatBotStandard()

    @staticmethod
    def get_chatbot(cls, name: str) -> ChatBotBase:
        if name == 'free':
            if ChatBotFactory.free_chatbot is None:
                ChatBotFactory.free_chatbot = ChatBotFree()
            return ChatBotFactory.free_chatbot
        elif name == 'standard':
            if ChatBotFactory.standard_chatbot is None:
                ChatBotFactory.standard_chatbot = ChatBotStandard()
            return ChatBotFactory.standard_chatbot
        else:
            raise ValueError('Invalid chatbot name')
