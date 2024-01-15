from aiogram import enums
from aiogram.types import InputMediaPhoto
from utils.db_requests import get_all_confirmed_users


async def all_confirmed_users_messenger(files_id, caption, bot):
    users = get_all_confirmed_users()

    for user in users:
        tg_id = user.telegram_id
        try:
            chat = await bot.get_chat(tg_id)
            if not chat.id:
                print(f"Бот не может отправлять сообщения в чат {tg_id}.")
                continue

            if files_id:
                photos = [
                    InputMediaPhoto(media=file_id, caption=caption if idx == 0 else None)
                    for idx, file_id in enumerate(files_id)
                ]
                await bot.send_media_group(tg_id, photos, parse_mode=enums.ParseMode.HTML)
            else:
                await bot.send_message(tg_id, caption, parse_mode=enums.ParseMode.HTML)

        except Exception as e:
            print(f"Произошла ошибка при отправке в чат {tg_id}: {e}")