from pydantic import BaseModel
from typing import Optional


class CompanyDomainBase(BaseModel):
    company: str
    domain: str
    short_cut: Optional[str] = None


class CompanyDomainCreate(CompanyDomainBase):
    pass


class CompanyDomainUpdate(CompanyDomainBase):
    company: Optional[str] = None
    domain: Optional[str] = None
