from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# State Database setup
state_engine = create_async_engine(
    settings.get_state_db_url(), 
    connect_args={"check_same_thread": False}
)
StateSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=state_engine, class_=AsyncSession)

# Memory Database setup
memory_engine = create_async_engine(
    settings.get_memory_db_url(), 
    connect_args={"check_same_thread": False}
)
MemorySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=memory_engine, class_=AsyncSession)

Base = declarative_base()

async def get_state_db():
    async with StateSessionLocal() as db:
        yield db

async def get_memory_db():
    async with MemorySessionLocal() as db:
        yield db
