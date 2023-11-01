from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import Database

db = Database()

db_dependency = Annotated[Session, Depends(db.get_db_session)]
