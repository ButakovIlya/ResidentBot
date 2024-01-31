from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.methods.send_media_group import SendMediaGroup
from utils.db_requests import get_user_by_id, get_all_tickets_by_user_id
from handlers.localization import Lang
import json


async def send_ticket_images_to_user(object, bot, user_id, text, issue_item):

    object_image = None

    issue_buttons = []
    if not issue_item.is_solved:
        close_ticket_button = InlineKeyboardButton(text=f"Отменить заявку", callback_data=f"delete_ticket_{issue_item.ticket_id}")
        issue_buttons.append([close_ticket_button])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=issue_buttons)

    if object.images:
        if not isinstance(object.images, str):
            object_image = object.images
        else:
            object_image = json.loads(object.images.replace("'", '"'))

    if object_image:
        photos = []
        for image in object_image:
            for k, v in image.items():
                photos.append(InputMediaPhoto(media=v, caption=text if k == "image1" else None))

        await bot.send_media_group(user_id, photos)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)
    else:
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)

async def send_ticket_images_to_employer(object, bot, user_id, text, issue_item):
    user = get_user_by_id(issue_item.user_id)
    object_image = None

    if object.images:
        if not isinstance(object.images, str):
            object_image = object.images
        else:
            object_image = json.loads(object.images.replace("'", '"'))

    issue_buttons = []
    user_profile_button = InlineKeyboardButton(text=f"Открыть профиль {user.username}", callback_data=f"profile_user_{user.telegram_id}")
    return_to_user_tickets_button = InlineKeyboardButton(text=f"Вернуться к заявкам {user.username}", callback_data=f"check_user_tickets_{user.telegram_id}")
    if not issue_item.is_solved:
        close_ticket_button = InlineKeyboardButton(text=f"Закрыть заявку", callback_data=f"close_ticket_{issue_item.ticket_id}")
        issue_buttons.append([close_ticket_button])

    issue_buttons.append([return_to_user_tickets_button])
    issue_buttons.append([user_profile_button])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=issue_buttons)
    
    if object_image:
        photos = []
        for image in object_image:
            for k, v in image.items():
                caption = text if k == "image1" else None
 
                photo = InputMediaPhoto(media=v, caption=caption, parse_mode='HTML')
                photos.append(photo)

        await bot.send_media_group(user_id, photos)
        await bot.send_message(user_id, f"Заявка от @{user.username}", reply_markup=keyboard_markup)
    else:
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)
