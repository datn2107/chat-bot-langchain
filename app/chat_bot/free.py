
from .base import ChatBotBase


class ChatBotFree(ChatBotBase):
    def __init__(
        self, debug=False
    ):
        super().__init__(debug=debug)
