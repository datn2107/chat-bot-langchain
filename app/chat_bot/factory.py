from .base import ChatBotBase
from .free import ChatBotFree
from .standard import ChatBotStandard


class ChatBotFactory:
    free_chatbot = ChatBotFree()
    standard_chatbot = ChatBotStandard()

    @staticmethod
    def get_chatbot(name: str, debug: bool = False) -> ChatBotBase:
        if name == "Free":
            if ChatBotFactory.free_chatbot is None:
                ChatBotFactory.free_chatbot = ChatBotFree(debug=debug)
            return ChatBotFactory.free_chatbot
        elif name == "Standard" or name == "Premium":
            if ChatBotFactory.standard_chatbot is None:
                ChatBotFactory.standard_chatbot = ChatBotStandard(debug=debug)
            return ChatBotFactory.standard_chatbot
        else:
            raise ValueError("Invalid chatbot name")
