# app/schemas.py


from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CreateAdvertisementRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)
    author: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)


class CreateAdvertisementResponse(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    author: str
    create_date: datetime


class UpdateAdvertisementRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    price: Optional[Decimal] = Field(default=None, gt=0)


class UpdateAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    create_date: str


class OKResponse(BaseModel):
    status: str = "ok"
