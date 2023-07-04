from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services import commit_refresh


class Investment:

    crud_objects = {
        'donation': donation_crud,
        'project': charity_project_crud
    }

    def _is_invested(
        self,
        object_: Union[CharityProject, Donation]
    ) -> None:
        object_.fully_invested = True
        object_.close_date = datetime.now()

    async def launch_investment(
        self,
        object_in: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        _type = 'project' if isinstance(object_in, Donation) else 'donation'
        objects = await self.crud_objects[_type].get_opened_objects(session)
        for object_ in objects:
            if object_in.full_amount > object_in.invested_amount:
                amount_required = object_.full_amount - object_.invested_amount
                if object_in.full_amount > amount_required:
                    object_in.invested_amount += amount_required
                else:
                    object_in.invested_amount = object_in.full_amount
                    self._is_invested(object_in)
                    object_.invested_amount += object_in.full_amount
                    if object_.invested_amount == object_.full_amount:
                        self._is_invested(object_)
                session.add(object_)
        await commit_refresh(object_in, session)
        return object_in
