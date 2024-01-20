from utils.db_requests import get_news_by_id, delete_news_by_id, get_all_news
from handlers.news import *
from utils.db_image_loader import send_news_images_to_user, send_news_images_to_employer
from buttons.emploee_menu import emploee_menu_markup 

async def change_news_page_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    current_page = await state.get_state() or 0
    all_news = get_all_news()
    pages = [all_news[i:i + 5] for i in range(0, len(all_news), 5)]

    if callback_query.data == "prev_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_state(current_page)

    await get_news_for_user(user_id, bot, state)

    await bot.delete_message(user_id, message_id)


async def show_news_details_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    news_id = int(callback_query.data.split("_")[1])
    news_item = get_news_by_id(news_id)

    # fix only photo 

    if news_item:
        news_details = f"Заголовок: {news_item.topic}\n\n{news_item.body}"

        await send_news_images_to_user(news_item, bot, user_id, news_details)
       
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)


async def edit_news_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    news_id = int(callback_query.data.split("_")[2])
    news_item = get_news_by_id(news_id)

    # fix only photo 

    if news_item:
        news_details = f"Заголовок: {news_item.topic}\n\n{news_item.body}"

        await send_news_images_to_employer(news_item, bot, user_id, news_details, news_item)
       
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)


async def delete_news_func(callback_query, state, bot):
    from_user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    news_id = int(callback_query.data.split("_")[2])
    news_item = get_news_by_id(news_id)

    if news_item:
        delete_news_by_id(news_id)
        await bot.send_message(from_user_id, f"Новость успешно удалена.", reply_markup=emploee_menu_markup)

    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["news_delete_error"])

    await bot.delete_message(from_user_id, message_id)