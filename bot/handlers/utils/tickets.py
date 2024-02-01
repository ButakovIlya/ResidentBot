from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.db_requests import get_user_by_id
import json


async def send_ticket_images_to_user(bot, text, issue_item, chat_id=None):
    object_image = None

    if issue_item.images:
        if not isinstance(issue_item.images, str):
            object_image = issue_item.images
        else:
            object_image = json.loads(issue_item.images.replace("'", '"'))


    user_id = issue_item.user_id
    issue_buttons = []
    if not issue_item.is_solved:
        close_ticket_button = InlineKeyboardButton(text=f"Отменить заявку", callback_data=f"delete_ticket_{issue_item.ticket_id}")
        issue_buttons.append([close_ticket_button])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=issue_buttons)

    photos = []
    if object_image:
        for image in object_image:
            for k, v in image.items():
                caption = text if k == "image1" else None
                photo = InputMediaPhoto(media=v, caption=caption, parse_mode='HTML')
                photos.append(photo)


        media_group_result = await bot.send_media_group(user_id, photos)

        if isinstance(media_group_result, list) and media_group_result:
            message_id = media_group_result[0].message_id

            caption = text + f"\n\nВыберите нужное для взаимодействия с заявкой"
            if len(media_group_result) == 1:
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption,
                                               reply_markup=keyboard_markup, parse_mode='HTML')
            else:

                await bot.send_message(user_id, f"Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)

    else:
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)

async def send_ticket_images_to_employer(object, bot, user_id, text, issue_item, state, chat_id):
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
    
    photos = []
    if object_image:
        for image in object_image:
            for k, v in image.items():
                caption = text if k == "image1" else None
                photo = InputMediaPhoto(media=v, caption=caption, parse_mode='HTML')
                photos.append(photo)


        media_group_result = await bot.send_media_group(user_id, photos)

        if isinstance(media_group_result, list) and media_group_result:
            message_id = media_group_result[0].message_id

            caption = text + f"\n\nЗаявка от @{user.username}"
            if len(media_group_result) == 1:
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption,
                                               reply_markup=keyboard_markup, parse_mode='HTML')
            else:
                await state.set_data({
                    'message_to_delete':message_id
                })
                await bot.send_message(user_id, f"Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)

    else:
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с заявкой", reply_markup=keyboard_markup)
