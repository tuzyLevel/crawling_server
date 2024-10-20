import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_ADDRESS = os.getenv("DATABASE_ADDRESS")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER_NAME = os.getenv("DATABASE_USER_NAME")
DATABASE_USER_PASSWORD = os.getenv("DATABASE_USER_PASSWORD")
DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER_NAME}:{
    DATABASE_USER_PASSWORD}@{DATABASE_ADDRESS}/{DATABASE_NAME}"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        session.commit()
