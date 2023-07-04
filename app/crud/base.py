from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.services import commit_refresh


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create(
        self,
        object_in: dict,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> Union[CharityProject, Donation]:
        object_in_dict = object_in.dict()
        if user is not None:
            object_in_dict["user_id"] = user.id
        object_ = self.model(**object_in_dict)
        await commit_refresh(object_, session)
        return object_

    async def get(
        self,
        object_id: int,
        session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        objects = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return objects.scalars().first()

    async def get_multi(self, session: AsyncSession):
        objects = await session.execute(select(self.model))
        return objects.scalars().all()

    async def update(
        self,
        object_: Union[CharityProject, Donation],
        object_in: Union[CharityProject, Donation],
        session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        object_data = jsonable_encoder(object_)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(object_, field, update_data[field])
        await commit_refresh(object_, session)
        return object_

    async def remove(
        self,
        object_,
        session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        await session.delete(object_)
        await session.commit()
        return object_

    async def get_opened_objects(
            self,
            session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        opened_objects = await session.execute(
            select(self.model).where(
                not_(self.model.fully_invested)).order_by(self.model.create_date)
        )
        return opened_objects.scalars().all()
