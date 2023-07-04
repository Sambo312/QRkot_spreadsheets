from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import GoogleApiMethods

router = APIRouter()
google_api = GoogleApiMethods()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_duration(session)
    spreadsheet_id = await google_api.spreadsheets_create(wrapper_services)
    await google_api.set_user_permissions(spreadsheet_id, wrapper_services)
    await google_api.spreadsheets_update_value(
        spreadsheet_id, projects, wrapper_services
    )
    return projects
