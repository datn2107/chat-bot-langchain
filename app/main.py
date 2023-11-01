import os
import sys
import dotenv
import logging
from typing import Tuple
from fastapi import FastAPI, HTTPException, Depends, status

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv.load_dotenv()

from config import db_dependency
from models import MessageHistory
from chat_bot import ChatBotFactory
from dependencies import jwt_dependency
from internal.message_history_repository import count_message_last_3_hours

logging.basicConfig(filename="app.log", filemode="a", level=logging.DEBUG)
app = FastAPI()


@app.get("/message/get", status_code=status.HTTP_200_OK)
async def get_message(
    db: db_dependency,
    user_email_type: Tuple[str, str] = jwt_dependency,
    skip: int = 0,
    limit: int = 10,
):
    try:
        messages = (
            db.query(MessageHistory)
            .filter(MessageHistory.user_email == user_email_type[0])
            .order_by(MessageHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as e:
        logging.info(
            "Get Messages {email}: {exception}".format(
                email=user_email_type[0], exception=str(e)
            )
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    if messages is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return messages


@app.post("/message/ask", status_code=status.HTTP_200_OK)
async def ask_message(
    message: str, db: db_dependency, user_email_type: Tuple[str, str] = jwt_dependency
):
    user_email, user_type = user_email_type

    number_of_messages = count_message_last_3_hours(user_email)
    if user_type == "Free" and number_of_messages >= 20:
        raise HTTPException(
            status_code=429,
            detail="You have reached the limit of 20 messages per 3 hours",
        )
    if user_type == "Premium" and number_of_messages >= 100:
        raise HTTPException(
            status_code=429,
            detail="You have reached the limit of 100 messages per 3 hours",
        )

    try:
        chat_bot = ChatBotFactory.get_chatbot(name=user_type)
        chat_bot.load_memory(user_email)
        response = await chat_bot.ask(user_email, message)
    except Exception as e:
        logging.info(
            "Ask Message {email}-{type}: {exception}".format(
                email=user_email, type=user_type, exception=str(e)
            )
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    return response
