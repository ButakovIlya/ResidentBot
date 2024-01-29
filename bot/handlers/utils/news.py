from aiogram.types import InputMediaPhoto, InputMediaVideo, InlineKeyboardMarkup, InlineKeyboardButton
import json

async def send_news_media_to_user(object, bot, user_id, text):

    object_media = None

    if object.media:
        if not isinstance(object.media, str):
            object_media = object.media
        else:
            object_media = json.loads(object.media.replace("'", '"'))

    if object_media:
        media_list = []
        for media_item in object_media:
            for key, path in media_item.items():
                print(key)
                if key.startswith("photo"):
                    media_list.append(InputMediaPhoto(media=path, caption=text if key == "image1" else None))
                elif key.startswith("video"):
                    media_list.append(InputMediaVideo(media=path, caption=text if key == "image1" else None))

        await bot.send_media_group(user_id, media_list)
    else:
        await bot.send_message(user_id, text)


async def send_news_images_to_employer(object, bot, user_id, text, news_item):

    object_image = None

    if object.images:
        if not isinstance(object.images, str):
            object_image = object.images
        else:
            object_image = json.loads(object.images.replace("'", '"'))

    news_buttons = []
    delete_news_button = InlineKeyboardButton(text=f"Удалить новость", callback_data=f"delete_news_{news_item.news_id}")
    news_buttons.append([delete_news_button])
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=news_buttons)

    if object_image:
        photos = []
        for image in object_image:
            for k, v in image.items():
                photos.append(InputMediaPhoto(media=v, caption=text if k == "image1" else None))

        await bot.send_media_group(user_id, photos)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с новостью", reply_markup=keyboard_markup)
    else:
        await bot.send_message(user_id, text)
        await bot.send_message(user_id, "Выберите нужное для взаимодействия с новостью", reply_markup=keyboard_markup)

