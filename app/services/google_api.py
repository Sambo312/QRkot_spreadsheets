from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


class GoogleApiMethods:

    api = {
        'drive': ['drive', 'v3'],
        'sheets': ['sheets', 'v4'],
    }
    permission_settings = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    sheet_settings = {
        'locale': 'ru_RU',
        'sheetType': 'GRID',
        'sheetId': 0,
        'rowCount': 50,
        'columnCount': 5,
        'majorDimension': 'ROWS'
    }

    def now(self):
        return datetime.now().isoformat(timespec='minutes')

    async def spreadsheets_create(self, wrapper_services: Aiogoogle) -> str:
        service = await wrapper_services.discover(
            self.api['sheets'][0],
            self.api['sheets'][1]
        )
        spreadsheet_body = {
            'properties': {
                'title': f'Отчет сервиса QRkot на {self.now()}',
                'locale': self.sheet_settings['locale']
            },
            'sheets': [
                {
                    'properties': {
                        'sheetType': self.sheet_settings['sheetType'],
                        'sheetId': self.sheet_settings['sheetId'],
                        'title': 'Рейтинг проектов по скорости закрытия',
                        'gridProperties': {
                            'rowCount': self.sheet_settings['rowCount'],
                            'columnCount': self.sheet_settings['columnCount']
                        }
                    }
                }
            ]
        }
        response = await wrapper_services.as_service_account(
            service.spreadsheets.create(json=spreadsheet_body)
        )
        return response['spreadsheetId']

    async def set_user_permissions(
            self,
            spreadsheet_id: str,
            wrapper_services: Aiogoogle
    ) -> None:
        service = await wrapper_services.discover(
            self.api['drive'][0],
            self.api['drive'][1]
        )
        await wrapper_services.as_service_account(
            service.permissions.create(
                fileId=spreadsheet_id,
                json=self.permission_settings,
                fields="id"
            )
        )

    async def spreadsheets_update_value(
        self,
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
    ) -> None:
        service = await wrapper_services.discover(
            self.api['sheets'][0],
            self.api['sheets'][1]
        )
        table_values = [
            ['Отчет от', self.now()],
            ['Список проектов:'],
            ['Название проекта', 'Время сбора', 'Описание']
        ]
        for project in projects:
            table_values.append(
                project['name'],
                project['duration'],
                project['description']
            )
        update_body = {
            'majorDimension': self.sheet_settings['majorDimension'],
            'values': table_values
        }
        await wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range=f'A1:C{len(table_values)}',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
