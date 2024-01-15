from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from handlers.localization import Lang
from utils.db_requests import get_employer_by_id

class EmployeeMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        tg_id = event.from_user.id

        employer = get_employer_by_id(tg_id)

        if (employer and employer.is_confirmed):
            return await handler(event, data)
        else:
            await event.bot.send_message(tg_id, Lang.strings["ru"]["employee_access_error"])
