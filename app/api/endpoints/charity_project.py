from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import CharityProjectValidators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectUpdate,
    CreateCharityProject,
)
from app.services.investment import Investment


router = APIRouter()
validator = CharityProjectValidators()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CreateCharityProject,
    session: AsyncSession = Depends(get_async_session),
):
    await validator.check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await Investment().launch_investment(new_project, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await validator.check_project_exists(project_id, session)
    validator.check_project_closed_or_invested(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await validator.check_name_duplicate(obj_in.name, session)
    charity_project = await validator.check_project_exists(project_id, session)
    validator.check_project_fully_invested(charity_project)
    validator.check_project_amount(obj_in, charity_project)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
