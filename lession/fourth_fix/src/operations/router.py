import time
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Идут вычисления..."
    

# ORM - Object-Relational Mapping, рус. объектно-реляционное отображение, 
# или преобразование — технология программирования, 
# которая связывает базы данных с концепциями объектно-ориентированных языков программирования
# SQL injection - SQL-инъекция (SQLi) - это уязвимость веб-безопасности, 
# которая позволяет злоумышленнику вмешиваться в запросы, 
# которые приложение делает к своей базе данных

### Пунктуация:
# query - если это SELECT
# stmt - если это INSERT DELETE ...

# Хочу использовать return result.all(), но он выдает 500 ошибку
# return result.scalars().all() # Возвращает только первое значение (в нашем случае id записи)
# Работоспособный вариант:
# data = [row._asdict() for row in result.all()]
# return {
#     "status": "success",
#     "data": data,
#     "details": None
# }

@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        data = [row._asdict() for row in result.all()]
        return {
            "status": "success",
            "data": data,
            "details": None 
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "Данные добавлены"}
