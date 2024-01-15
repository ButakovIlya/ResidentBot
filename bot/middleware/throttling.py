import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class CancelHandler(Exception):
    pass


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit=5, reset_time=10):
        self.user_message_count = {}
        self.limit = limit
        self.user_warned = {}
        self.reset_time = reset_time

    async def clear_user_count(self, user_id, event):
        await asyncio.sleep(self.reset_time)
        if user_id in self.user_message_count:
            del self.user_message_count[user_id]
            if user_id in self.user_warned:
                del self.user_warned[user_id]
                await event.reply("Вы снова можете отправлять сообщения !")

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> None:
        if event.content_type not in ['text']:
            await handler(event, data)
            return
        user_id = event.from_user.id
        limit = self.limit

        if user_id not in self.user_message_count:
            self.user_message_count[user_id] = 1
        else:
            self.user_message_count[user_id] += 1

        if user_id in self.user_warned:
            return CancelHandler()

        if self.user_message_count[user_id] > limit:
            await event.reply("Вы отправляете слишком много сообщений. Пожалуйста, перестаньте спамить.")
            self.user_warned[user_id] = True

        asyncio.create_task(self.clear_user_count(user_id, event))

        await handler(event, data)
