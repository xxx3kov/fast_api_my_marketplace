# app/schemas.py


from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal


class CreateAdvertisementResponse(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: Decimal
    create_date: Optional[str] = None


class UpdateAdvertisementRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None


class UpdateAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: Decimal
    create_date: Optional[str] = None


class OKResponse(BaseModel):
    status: str = "ok"
