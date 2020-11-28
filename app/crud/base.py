import pendulum
from datetime import datetime
from sqlalchemy import DateTime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..storage.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        
    @staticmethod
    def _encode(obj_in: Union[ModelType, CreateSchemaType, UpdateSchemaType, Dict[str, Any]]) -> Dict[str, Any]:
        
        def convert(x: Dict[str, Any]) -> Dict[str, Any]:
            y = {}
            for k, v in x.items():
                if isinstance(v, dict):
                    v = convert(v)
                elif isinstance(v, str):
                    try:
                        v = pendulum.parse(v).replace(tzinfo=None) 
                    except Exception as e:
                        pass
                    
                elif isinstance(v, datetime):
                       v = v.replace(tzinfo=None) 
                y[k] = v
            return y
        
        # FIXME: hack until fixed in sqlalchemy
        obj_in_data = jsonable_encoder(obj_in)
        return convert(obj_in_data)

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        db_execute = await db.execute(select(self.model).filter(self.model.id == id))
        return db_execute.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await db.exectue(select(self.model).offset(skip).limit(limit)).scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = self._encode(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = self._encode(db_obj)
        obj_in = self._encode(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        db_execute =  await db.execute(select(self.model).filter(self.model.id == id))
        obj = db_execute.scalars().one_or_none()
        db.delete(obj)
        await db.commit()
        return obj
