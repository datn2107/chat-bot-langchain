import os
import sys
import dotenv
from fastapi import FastAPI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv.load_dotenv()

from config import db_dependency
from models import Base

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
