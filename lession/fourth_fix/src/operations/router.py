from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

# ORM - Object-Relational Mapping, рус. объектно-реляционное отображение, 
# или преобразование — технология программирования, 
# которая связывает базы данных с концепциями объектно-ориентированных языков программирования
# SQL injection - SQL-инъекция (SQLi) - это уязвимость веб-безопасности, 
# которая позволяет злоумышленнику вмешиваться в запросы, 
# которые приложение делает к своей базе данных

### Пунктуация:
# query - если это SELECT
# stmt - если это INSERT DELETE ...


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    # print(query) # таким способом, можем посмотреть query в cmd
    result = await session.execute(query)
    # Хочу использовать return result.all(), но он выдает 500 ошибку
    # return result.scalars().all() # Возвращает только первое значение (в нашем случае id записи)
    # Работоспособный вариант:
    data = [row._asdict() for row in result.all()]
    return {
        "status": "success",
        "data": data,
        "details": None
    }

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "Данные добавлены"}
