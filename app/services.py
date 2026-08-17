# app/services.py
from decimal import Decimal
from typing import Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schema


async def add_item(
    session: AsyncSession,
    orm_model: type[models.Advertisement],
    item_data: schema.CreateAdvertisementRequest,
) -> models.Advertisement:
    """
    Универсальная функция для добавления записи в БД.
    """
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as e:
        await session.rollback()
        # Проверяем, является ли ошибка нарушением уникальности (код 23505 для PostgreSQL)
        if isinstance(e.orig, UniqueViolationError) and e.orig.pgcode == "23505":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with such data already exists.",
            )
        else:
            # Если это другая ошибка целостности, пробрасываем её дальше
            raise e


async def get_advertisement_id(
    session: AsyncSession, orm_model: type[models.Advertisement], item_id: int
) -> models.Advertisement:
    """
    Получает запись по ID или выбрасывает 404.
    """
    stmt = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found",
        )
    return item


async def get_advertisements(
    session: AsyncSession,
    orm_model: type[models.Advertisement],
    title: Optional[str] = None,
    description: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
):
    stmt = select(orm_model)

    # Поиск по подстроке в названии
    if title is not None:
        stmt = stmt.where(orm_model.title.ilike(f"%{title}%"))

    # Поиск по описанию
    if description is not None:
        stmt = stmt.where(orm_model.description.ilike(f"%{description}%"))

    # Поиск по диапазону в цене
    if min_price is not None:
        stmt = stmt.where(orm_model.price >= min_price)

    if max_price is not None:
        stmt = stmt.where(orm_model.price <= max_price)

    stmt = stmt.order_by(orm_model.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_item(
    session: AsyncSession,
    orm_model: type[models.Advertisement],
    item_id: int,
    update_data: schema.UpdateAdvertisementRequest,
) -> models.Advertisement:
    """
    Обновляет запись. .
    """
    item = await get_advertisement_id(session, orm_model, item_id)

    # Преобразуем update_data в словарь, исключая поля со значением None
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
    session: AsyncSession, orm_model: type[models.Advertisement], item_id: int
) -> None:
    """
    Удаляет запись.
    """
    item = await get_advertisement_id(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()
