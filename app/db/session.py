from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# State Database setup
state_engine = create_engine(
    settings.get_state_db_url(), 
    connect_args={"check_same_thread": False}
)
StateSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=state_engine)

# Memory Database setup
memory_engine = create_engine(
    settings.get_memory_db_url(), 
    connect_args={"check_same_thread": False}
)
MemorySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=memory_engine)

Base = declarative_base()

def get_state_db():
    db = StateSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_memory_db():
    db = MemorySessionLocal()
    try:
        yield db
    finally:
        db.close()
