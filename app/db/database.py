import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


from dotenv import load_dotenv

load_dotenv()

DATABASE_DOMAIN = os.getenv("DATABASE_DOMAIN")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER_NAME = os.getenv("DATABASE_USER_NAME")
DATABASE_USER_PASSWORD = os.getenv("DATABASE_USER_PASSWORD")
DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER_NAME}"\
    f":{DATABASE_USER_PASSWORD}@{DATABASE_DOMAIN}:{DATABASE_PORT}/{DATABASE_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True,
                             pool_pre_ping=True,  # 연결 상태 확인
                             pool_recycle=3600,   # 연결 재활용 시간
                             pool_size=5,         # 연결 풀 크기
                             max_overflow=10)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
