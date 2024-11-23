from fastapi import APIRouter
from fastapi import Depends
from app.utils.common import get_current_user
from .functions import get_companys, insert_companys
from .schemas import CompanyDomainCreate, CompanyDomainUpdate

router = APIRouter()


@router.post("")
async def create_company(request_data: CompanyDomainCreate, _=Depends(get_current_user)):
    return await insert_companys(request_data.model_dump())


@router.get("")
async def read_companys(_=Depends(get_current_user)):
    return await get_companys()


@router.get("/{company_name}")
def get_company(company_name: str, _=Depends(get_current_user)):
    return "company"


@router.patch("")
async def update_companys(
    request_data: CompanyDomainUpdate, _=Depends(get_current_user)): pass
