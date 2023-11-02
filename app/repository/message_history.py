import logging
from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from models import MessageHistory, MessageType
from config import db


class MessageHistoryRepository:
    db_session: Session = None


    def __init__(self):
        self.db_session = self.open_db_session()


    def open_db_session(self):
        db_session = next(db.get_db_session())
        return db_session


    def get_messages(
        self, user_email: str, skip: int = 0, limit: int = 10
    ) -> Optional[List[MessageHistory]]:
        try:
            messages = (
                self.db_session.query(MessageHistory)
                .filter(MessageHistory.user_email == user_email)
                .order_by(MessageHistory.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except Exception as e:
            logging.debug(
                "Get Messages {email}: {exception}".format(
                    email=user_email, exception=str(e)
                )
            )
            raise e

        return messages


    def clear_messages(self, user_email: str):
        try:
            self.db_session.query(MessageHistory).filter(
                MessageHistory.user_email == user_email
            ).delete()
            self.db_session.commit()
        except Exception as e:
            logging.debug(
                "Clear Messages {email}: {exception}".format(
                    email=user_email, exception=str(e)
                )
            )
            self.db_session.rollback()
            raise e


    def get_last_k_messages(
        self, user_email: str, k: int = 10
    ) -> Optional[List[MessageHistory]]:
        try:
            messages = (
                self.db_session.query(MessageHistory)
                .filter(MessageHistory.user_email == user_email)
                .order_by(MessageHistory.created_at.desc())
                .limit(k)
                .all()
            )
        except Exception as e:
            logging.debug(
                "Get {k} Last Messages {email}: {exception}".format(
                    k=k, email=user_email, exception=str(e)
                )
            )
            raise e

        return messages


    def add_message(
        self, user_mail: str, content: str, message_type: MessageType
    ) -> Optional[MessageHistory]:
        try:
            message_history = MessageHistory(
                user_email=user_mail, content=content, message_type=message_type
            )

            self.db_session.add(message_history)
            self.db_session.commit()
            return message_history
        except Exception as e:
            logging.debug(
                "Add Message {email}|{message}|{message_type}: {exception}".format(
                    email=user_mail,
                    message=content,
                    message_type=message_type,
                    exception=str(e),
                )
            )
            self.db_session.rollback()
            raise e


    def count_message_last_k_hours(self, user_email: str, k: int = 3) -> int:
        try:
            count = (
                self.db_session.query(MessageHistory)
                .filter(MessageHistory.user_email == user_email)
                .filter(
                    MessageHistory.created_at > text("DATE_SUB(NOW(), INTERVAL 3 HOUR)")
                )
                .count()
            )
        except Exception as e:
            logging.debug(
                "Count Message Last 3 Hours {email}: {exception}".format(
                    email=user_email, exception=str(e)
                )
            )
            raise e

        return count


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    from dotenv import load_dotenv

    load_dotenv()

    messages_history_repository = MessageHistoryRepository()

    print(
        messages_history_repository.add_message(
            user_mail="khoa@gmail.com", content="Hello", message_type="AI"
        )
    )

    messages = messages_history_repository.get_last_10_messages("khoa@gmail.com")
    print(messages)
