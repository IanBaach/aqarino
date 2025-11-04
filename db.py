from sqlmodel import SQLModel, create_engine, Session
import os
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./aqarino_v2.db")
engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
