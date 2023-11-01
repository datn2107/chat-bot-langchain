import os
import sys
import dotenv
import logging
from fastapi import FastAPI, HTTPException, Depends, status

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv.load_dotenv()

from config import db_dependency
from models import MessageHistory
from dependencies import jwt_dependency

logging.basicConfig(filemode="w+", level=logging.DEBUG)
app = FastAPI()


@app.get("/message/get", status_code=status.HTTP_200_OK)
async def get_message(db: db_dependency, user_email: str = jwt_dependency, skip: int = 0, limit: int = 10):
    try:
        messages = (
            db.query(MessageHistory)
            .filter(MessageHistory.user_email == user_email)
            .order_by(MessageHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as e:
        logging.info("Get Messages {email}: {exception}".format(email=user_email, exception=str(e)))
        raise HTTPException(status_code=500, detail="Internal server error")

    if messages is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return messages


@app.post("/message/ask", status_code=status.HTTP_200_OK)
async def ask_message(message: str, db: db_dependency, user_email: str = jwt_dependency):
    pass


@app.get('/me', summary='Get details of currently logged in user', status_code=status.HTTP_200_OK)
async def get_me(email: str = jwt_dependency):
    return email
