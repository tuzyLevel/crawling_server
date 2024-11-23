from typing import Dict
from app.db.database import get_db
from app.db.company_domains.crud import get_company_domains, insert_company_domain


async def get_companys(skip: int = 0, limit: int = 100):

    async with get_db() as session:
        return await get_company_domains(db=session, skip=skip, limit=limit)


async def insert_companys(data: Dict):
    async with get_db() as session:
        return await insert_company_domain(db=session, data=data)


# async def update_companys(data: Dict):
#     async with get_db() as session:
#         return await update_company(db=session, data=data)
