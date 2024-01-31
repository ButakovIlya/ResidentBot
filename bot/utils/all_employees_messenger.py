from aiogram.types import InputMediaPhoto
from utils.db_requests import get_all_employers_ids

async def all_employees_messenger(files_id, caption, bot, logger):
    employers = get_all_employers_ids()

    for employer_id in employers:
        try:
            chat = await bot.get_chat(employer_id)
            if not chat.id:
                logger.error(f"Бот не может отправлять сообщения в чат {employer_id}.")
                continue

            if files_id:
                photos = [
                    InputMediaPhoto(media=file_id, caption=caption if idx == 0 else None)
                    for idx, file_id in enumerate(files_id)
                ]
                await bot.send_media_group(employer_id, photos)
            else:
                await bot.send_message(employer_id, caption)

        except Exception as e:
            logger.error(f"Произошла ошибка при отправке в чат {employer_id}: {e}")