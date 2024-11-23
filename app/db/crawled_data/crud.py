from typing import List, Optional, Dict

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.crawled_data import CrawledData


async def insert_crawled_data(db: AsyncSession, data: Dict) -> bool:
    """insert crawled data"""

    stmt = insert(CrawledData)\
        .values(**data)

    await db.execute(stmt)
    return True
