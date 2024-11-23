from typing import List, Optional, Dict
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company_domain import CompanyDomain


async def insert_company_domain(db: AsyncSession, data: Dict) -> bool:
    """insert new company domain"""

    stmt = insert(CompanyDomain)\
        .values(**data)

    await db.execute(stmt)
    return True


async def get_company_domains(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[dict]:
    """Get list of company domains"""
    stmt = select(CompanyDomain)\
        .offset(skip)\
        .limit(limit)

    result = await db.execute(stmt)
    return [row.__dict__ for row in result.scalars().all()]


# async def update_company_domain(db: AsyncSession, data: Dict) -> bool:
#     """Update company domain"""
#     try:
#         stmt = update(CompanyDomain)\
#             .where(CompanyDomain.company == data.company)\
#             .values(**data)

#         await db.execute(stmt)
#         return True
#     except:

#         return False


# def delete_company_domain(db: Session, domain: str) -> bool:
#     """Delete company domain"""
#     try:
#         db.execute(
#             "DELETE FROM company_domains WHERE domain = :domain",
#             {"domain": domain}
#         )
#         db.commit()
#         return True
#     except:
#         db.rollback()
#         return False
