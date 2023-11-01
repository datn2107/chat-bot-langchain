import logging
from typing import List, Optional
from sqlalchemy import text

from app.models import MessageHistory, MessageType
from app.config.database import Database


def open_db_session():
    db = Database()
    db_session = next(db.get_db_session())
    return db_session


def get_last_10_messages(user_email: str) -> Optional[List[MessageHistory]]:
    try:
        db_session = open_db_session()
        messages = (
            db_session.query(MessageHistory)
            .filter(MessageHistory.user_email == user_email)
            .order_by(MessageHistory.created_at.desc())
            .limit(10)
            .all()
        )
    except Exception as e:
        logging.info(
            "Get 10 Last Messages {email}: {exception}".format(
                email=user_email, exception=str(e)
            )
        )
        return None

    return messages


def add_message(
    user_mail: str, content: str, message_type: MessageType
) -> Optional[MessageHistory]:
    try:
        db_session = open_db_session()
        message_history = MessageHistory(
            user_email=user_mail, content=content, message_type=message_type
        )

        db_session.add(message_history)
        db_session.commit()
        return message_history
    except Exception as e:
        logging.info(
            "Add Message {email}|{message}|{message_type}: {exception}".format(
                email=user_mail,
                message=content,
                message_type=message_type,
                exception=str(e),
            )
        )
        return None


def count_message_last_3_hours(user_email: str) -> int:
    try:
        db_session = open_db_session()
        count = (
            db_session.query(MessageHistory)
            .filter(MessageHistory.user_email == user_email)
            .filter(MessageHistory.created_at > text("DATE_SUB(NOW(), INTERVAL 3 HOUR)"))
            .count()
        )
    except Exception as e:
        logging.info(
            "Count Message Last 3 Hours {email}: {exception}".format(
                email=user_email, exception=str(e)
            )
        )
        return 0

    return count


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    from dotenv import load_dotenv

    load_dotenv()

    print(add_message(user_mail="khoa@gmail.com", content="Hello", message_type="AI"))
    
    messages = get_last_10_messages("khoa@gmail.com")
    print(messages)
