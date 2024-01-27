from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from handlers.localization import Lang

from db.db_config import User
from utils.db_requests import Session


class RegistrationMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        User.set_session(Session())
        tg_id = event.from_user.id
        user: User = User.get_user_by_id(tg_id)
        User.close_session()

        if (user is not None and user.is_confirmed) or event.text == "/start":
            if not user.is_banned:
                return await handler(event, data)
            else:
                await event.bot.send_message(tg_id, Lang.strings["ru"]["user_is_banned"])
        else:
            await event.bot.send_message(tg_id, Lang.strings["ru"]["employee_access_error"])
