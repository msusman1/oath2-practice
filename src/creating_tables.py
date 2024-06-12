
from fastapi import FastAPI
from src.database import engine
from contextlib import asynccontextmanager
from src.model import Users


def create_tables():
    Users.metadata.create_all(engine)
     
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("This statement will executes before the Creating tables....")
    create_tables()
    yield  
     
 