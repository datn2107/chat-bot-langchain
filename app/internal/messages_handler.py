import logging
from typing import List
from sqlalchemy.orm import Session

# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.models import MessageHistory

def get_last_10_messages(user_email: str, db_session: Session) -> List[MessageHistory]:
    try:
        messages = (
            db_session.query(MessageHistory)
            .filter(MessageHistory.user_email == user_email)
            .order_by(MessageHistory.created_at.desc())
            .limit(10)
            .all()
        )
    except Exception as e:
        logging.info("Get 10 Last Messages {email}: {exception}".format(email=user_email, exception=str(e)))
        return None

    return messages


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    from app.config.database import Database
    from app.config import db_dependency

    db = Database()
    db_session = db.get_db_session()
    db_session = next(db_session)

    messages = get_last_10_messages("khoa@gmail.com", db_session)
    print(messages)
