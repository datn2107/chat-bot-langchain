import os
import sys
import dotenv
import logging
from typing import Tuple
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv()

from models import MessageHistory
from chat_bot import ChatBotFactory
from dependencies import jwt_dependency
from repository import messages_history_repository

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/messages/get", status_code=status.HTTP_200_OK)
async def get_message(
    user_email_type: Tuple[str, str] = jwt_dependency,
    skip: int = 0,
    limit: int = 10,
):
    try:
        messages = messages_history_repository.get_messages(user_email_type[0], skip, limit)
    except Exception as e:
        logging.debug(
            "Get Messages {email}: {exception}".format(
                email=user_email_type[0], exception=str(e)
            )
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    if messages is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return messages


@app.delete("/messages/clear", status_code=status.HTTP_200_OK)
async def clear_message(user_email_type: Tuple[str, str] = jwt_dependency):
    try:
        messages_history_repository.clear_messages(user_email_type[0])
    except Exception as e:
        logging.debug(
            "Clear Messages {email}: {exception}".format(
                email=user_email_type[0], exception=str(e)
            )
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "Clear messages successfully"}


@app.get("/messages/ask", status_code=status.HTTP_200_OK)
async def ask_message(
    message: str, user_email_type: Tuple[str, str] = jwt_dependency
):
    user_email, user_type = user_email_type

    if user_type not in ["Free", "Standard", "Premium"]:
        raise HTTPException(
            status_code=400, detail="Error token: User type must be Free, Standard or Premium"
        )

    number_of_messages = messages_history_repository.count_message_last_k_hours(user_email, k=3)
    if user_type == "Free" and number_of_messages >= 20:
        raise HTTPException(
            status_code=429,
            detail="You have reached the limit of 20 messages per 3 hours",
        )
    if user_type == "Standard" and number_of_messages >= 100:
        raise HTTPException(
            status_code=429,
            detail="You have reached the limit of 100 messages per 3 hours",
        )
    if user_type == "Premium" and number_of_messages >= 200:
        raise HTTPException(
            status_code=429,
            detail="You have reached the limit of 200 messages per 3 hours",
        )

    try:
        chat_bot = ChatBotFactory.get_chatbot(name=user_type)
        chat_bot.load_memory(user_email)
        response = await chat_bot.ask(user_email, message)
    except Exception as e:
        logging.debug(
            "Ask Message {email}-{type}: {exception}".format(
                email=user_email, type=user_type, exception=str(e)
            )
        )
        raise HTTPException(status_code=500, detail="Internal server error")

    return response
