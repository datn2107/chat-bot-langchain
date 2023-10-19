from chat_bot import chatbot_factory
import dotenv

dotenv.load_dotenv()

bot = chatbot_factory('free')
print(bot)
