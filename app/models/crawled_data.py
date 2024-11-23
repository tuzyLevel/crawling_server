from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from ..db.database import Base


class CrawledData(Base):
    __tablename__ = "crawled_data"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    path = Column(String)
    params = Column(String)
    title = Column(String)
    thumbnail_url = Column(String)
    origin_price = Column(Integer)
    discounted_price = Column(Integer)
    discount_rate = Column(Float)
    is_deleted = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), default=func.now())
    updated_date = Column(DateTime(timezone=True),
                          server_onupdate=func.now())
