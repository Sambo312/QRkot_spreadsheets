from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services import force_int


class CharityProjectValidators:

    responses = {
        'duplicate': 'Проект с таким именем уже существует!',
        'exists': 'Проект не найден!',
        'closed': 'В проект были внесены средства, не подлежит удалению!',
        'invested': 'Закрытый проект нельзя редактировать!',
        'amount': 'Требуемая сумма меньше внесённой!'
    }

    async def check_name_duplicate(
        self,
        project_name: str, session: AsyncSession
    ) -> None:
        project_id = await charity_project_crud.get_project_id_by_name(
            project_name, session
        )
        if project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.responses['duplicate'],
            )

    async def check_project_exists(
        self,
        project_id: int, session: AsyncSession
    ) -> CharityProject:
        charity_project = await charity_project_crud.get(project_id, session)
        if charity_project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.responses['exists']
            )
        return charity_project

    def check_project_closed_or_invested(
        self,
        project: CharityProject
    ) -> None:
        if project.close_date is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.responses['closed']
            )

        if project.invested_amount > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.responses['closed']
            )

    def check_project_fully_invested(
        self,
        project: CharityProject
    ) -> None:
        if project.fully_invested:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.responses['invested']
            )

    def check_project_amount(
        self,
        object_in: CharityProject,
        project: CharityProject
    ) -> None:
        if force_int(object_in.full_amount) < force_int(project.invested_amount):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=self.responses['amount']
            )
