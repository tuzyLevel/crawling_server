from pydantic import BaseModel, Field
from typing import Optional


class CrawledDataBase(BaseModel):
    domain: str = Field(..., description="Crawling Domain")
    path: str | None = Field(None, description="Crawling Path")
    params: str | None = Field(None, dscription="Crawling params")
    title: str = Field(..., description="Data title")
    thumbnail_url: str = Field(..., description="Data Thumbnail Url")
    origin_price: int = Field(0, description="Original Price")
    discounted_price: int = Field(0, description="Discounted Price")
    discount_rate: float = Field(0.0, description="Discount Rate")
