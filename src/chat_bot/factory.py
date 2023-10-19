from .base import ChatBotBase
from .free import ChatBotFree
from .standard import ChatBotStandard

def chatbot_factory(name: str) -> ChatBotBase:
    if name == 'free':
        return ChatBotFree()
    elif name == 'standard':
        return ChatBotStandard()
    else:
        raise ValueError('Invalid chatbot name')
