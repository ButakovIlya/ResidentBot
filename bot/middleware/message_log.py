from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('../logs/telegram_bot.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(telegram_id)s @%(telegram_nickname)s %(levelname)s - [%(message)s]')
handler.setFormatter(formatter)

logger.addHandler(handler)

class MessagesLog(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> None:
        user_id = event.from_user.id
        user_name = event.from_user.username
        log_message = 'Received message from user %s: %s' % (user_id, event.text)
        logger.info(log_message, extra={'telegram_id': user_id, 'telegram_nickname': user_name})


        await handler(event, data)
        return data
