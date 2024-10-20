from fastapi import APIRouter
from .company_domain.router import router as company_domain_router


router = APIRouter()


router.include_router(company_domain_router, prefix="/company")
