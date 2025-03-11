from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_db_and_tables, drop_db_and_tables, fill_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    fill_db()
    yield
    drop_db_and_tables()

app = FastAPI(lifespan=lifespan)
