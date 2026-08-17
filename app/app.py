# app/app.py

from decimal import Decimal
from typing import Annotated, Optional

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schema
from dependencies import get_db_session
from lifespan import lifespan
from services import (
    add_item,
    get_advertisement_id,
    update_item,
    delete_item,
    get_advertisements,
)

app = FastAPI(
    title="My Marketplace",
    description="This is simple bulletin board",
    version="0.0.1",
    lifespan=lifespan,
)

SessionDep = Annotated(AsyncSession, Depends(get_db_session))


# Создание: POST /advertisement
@app.post(
    "/advertisement",
    response_model=schema.CreateAdvertisementResponse,
    summary="Создание объявления",
)
async def create_advertisement(
    advertisement_data: schema.CreateAdvertisementRequest, session: SessionDep
):
    new_advertisement = await add_item(
        session, models.Advertisement, advertisement_data
    )
    return schema.CreateAdvertisementResponse(id=new_advertisement.id)


# Обновление: PATCH /advertisement/{advertisement_id}
@app.patch(
    "/advertisement/{advertisement_id}",
    response_model=schema.UpdateAdvertisementResponse,
    summary="Обновить объявление",
)
async def update_advertisement(
    advertisement_id: int,
    update_data: schema.UpdateAdvertisementRequest,
    session: SessionDep,
):
    updated_advertisement = await update_item(
        session, models.Advertisement, advertisement_id, update_data
    )
    return schema.UpdateAdvertisementResponse(**updated_advertisement.to_dict())


# Удаление: DELETE /advertisement/{advertisement_id}
@app.delete(
    "/advertisement/{advertisement_id}",
    response_model=schema.OKResponse,
    summary="Удаление объявления",
)
async def delete_advertisement(advertisement_id: int, session: SessionDep):
    await delete_item(session, models.Advertisement, advertisement_id)
    return schema.OKResponse()


# Получение по id: GET  /advertisement/{advertisement_id}
@app.get(
    "/advertisement/{advertisement_id}",
    response_model=schema.GetAdvertisementResponse,
    summary="Получение объявления по ID",
)
async def get_for_id(advertisement_id: int, session: SessionDep):
    advertisement = await get_advertisement_id(
        session, models.Advertisement, advertisement_id
    )
    return schema.GetAdvertisementResponse(**advertisement.to_dict())


# Поиск по полям: GET /advertisement?{query_string}
@app.get(
    "/advertisement",
    response_model=list[schema.GetAdvertisementResponse],
    summary="Поиск объявлений по полям",
)
async def search_advertisements_qs(
    session: SessionDep,
    title: Optional[str] = None,
    description: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
):
    advertisements = await get_advertisements(
        session,
        models.Advertisement,
        title,
        description,
        min_price,
        max_price,
    )

    responses = [
        schema.GetAdvertisementResponse(**ads.to_dict()) for ads in advertisements
    ]

    return responses
