from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import Database

database = Database()

db_dependency = Annotated[Session, Depends([database.get_db_session])]
