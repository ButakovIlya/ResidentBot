from aiogram.types import InputMediaPhoto
import json
async def send_news_images_to_user(object, bot, user_id, text):

    object_image = None

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
    else:
        await bot.send_message(user_id, text)
