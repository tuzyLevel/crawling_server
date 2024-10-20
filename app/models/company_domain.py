from sqlalchemy import Column, Integer, String
from ..db.database import Base


class CompanyDomain(Base):
    __tablename__ = "company_domains"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    domain = Column(String)
    short_cut = Column(String)
