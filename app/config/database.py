import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class Database:
    engine: Engine = None
    session: Session = None

    def __init__(self):
        self.engine = self.get_db_engine()
        self.session_maker = sessionmaker(bind=self.engine)

    def get_db_engine(self) -> Engine:
        url = os.getenv('DB_URL')
        self.engine = create_engine(url)
        return self.engine

    def get_db_session(self) -> Session:
        db_session = self.session_maker()
        try:
            yield db_session
        finally:
            db_session.close()
