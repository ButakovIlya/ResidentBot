from aiogram import Router, types, enums, exceptions
from aiogram.fsm.context import FSMContext

from StateGroups.RegistrationEmplState import *
from StateGroups.RegistrationState import *
from buttons.emploee_menu import emploee_menu_markup
from buttons.main_menu import main_menu_markup
from buttons.registration import *
from dict.role_dict import *
from utils.db_requests import *
from utils.validation import is_valid_name, is_valid_email, is_valid_phone_number

registration_router = Router()

# Нейминг функций:

# <field_name>_selected()
# filed_name — поле, только что введённое пользователем
# то есть в названиях функций используется поле, которое было введено, а не которое требуется ввеси пользователю сейчас

# empl_ в названии означает принадлежность функции к регистрации сотрудника


@registration_router.callback_query(lambda query: query.data in empl_roles, RegistrationEmplState.email)
async def empl_role_selected(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.from_user.id

    role_id = get_employer_role_id_by_role_name(query.data)
    update_employer(tg_id, {"role_id": role_id})

    await empl_send_verification_request(tg_id, query.bot)

    await state.clear()
    await query.message.answer("Регистрация завершена. Данные отправлены на верификацию сотруднику управляющей компании")
    await query.answer()


async def empl_send_verification_request(unverified_empl_tg_id: int, bot):
    unverified_empl: Employer = get_employer_by_id(unverified_empl_tg_id)
    role_name = get_employer_role_by_id(unverified_empl.role_id).role

    message_text = (f"Новая заявка сотрудника:\n\n"
                    f"ФИО: {unverified_empl.last_name} {unverified_empl.first_name} {unverified_empl.patronymic}\n"
                    f"Номер телефона: {unverified_empl.phone_number}\n"
                    f"Email: {unverified_empl.email}\n"
                    f"Должность: {role_name}")

    # определение получателей
    directors = get_all_confirmed_employees_with_role("Директор")
    if role_name == "Директор" or len(directors) == 0:
        empl_recipients = get_all_confirmed_employees_with_role("Администратор")
    else:
        empl_recipients = directors

    # рассылка
    for recipient in empl_recipients:
        await send_message_to_empl(bot, recipient.telegram_id, message_text, reply_markup=await get_empl_verif_markup(unverified_empl_tg_id))


@registration_router.callback_query(lambda query: query.data.startswith("empl-verif-approve-"))
async def empl_approve_verif_request(query: types.CallbackQuery):
    tg_id = int(query.data[19:])
    empl = get_employer_by_id(tg_id)

    if empl.is_registration_reviewed:
        await query.answer('Заявку уже рассмотрел другой сотрудник')
        if empl.is_confirmed:
            new_text = '\n\n✅ Уже подтверждена другим сотрудником'
        else:
            new_text = '\n\n❌ Уже отклонена другим сотрудником'
        await query.bot.edit_message_text(query.message.text + new_text,
                                          query.message.chat.id, query.message.message_id)
    else:
        update_employer(tg_id, {"is_confirmed": True, "is_registration_reviewed": True})
        await query.bot.send_message(tg_id, "Ваша заявка (сотрудник) подтверждена", reply_markup=emploee_menu_markup)

        await query.bot.edit_message_text(query.message.text + '\n\n✅ Подтверждена',
                                          query.message.chat.id, query.message.message_id)


@registration_router.callback_query(lambda query: query.data.startswith('empl-verif-reject-'))
async def empl_reject_verif_request(query: types.CallbackQuery):
    tg_id = int(query.data[18:])

    empl = get_employer_by_id(tg_id)
    if empl.is_registration_reviewed:
        await query.answer('Заявку уже рассмотрел другой сотрудник')
        if empl.is_confirmed:
            new_text = '\n\n✅ Уже подтверждена другим сотрудником'
        else:
            new_text = '\n\n❌ Уже отклонена другим сотрудником'
        await query.bot.edit_message_text(query.message.text + new_text,
                                          query.message.chat.id, query.message.message_id)
    else:
        await query.bot.send_message(tg_id, "Ваша заявка (сотрудник) отклонена.\nДля изменения данных: /start")
        update_employer(tg_id, {"is_registration_reviewed": True})

        await query.bot.edit_message_text(query.message.text + '\n\n❌ Отклонена',
                                          query.message.chat.id, query.message.message_id)


@registration_router.message(RegistrationEmplState.phone_number)
async def empl_email_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    email = message.text

    if is_valid_email(email):
        update_employer(tg_id, {"email": email})
        await state.set_state(RegistrationEmplState.email)
        await message.answer('Выберите должность:', reply_markup=empl_roles_markup)
    else:
        await message.answer("Некорретный адрес.\nВведите ваш адрес электронной почты.")


@registration_router.message(RegistrationEmplState.full_name)
async def empl_phone_number_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    phone_number = message.text
    # если отправили чужой контакт или сообщение не того типа
    if not hasattr(message.contact, 'phone_number') or message.contact.user_id != message.from_user.id:
        await message.answer('Некорретный ввод. Кнопка ниже')
        return
    
    update_employer(tg_id, {"phone_number": message.contact.phone_number})
    await state.set_state(RegistrationEmplState.phone_number)
    await message.answer('Введите ваш адрес электронной почты.')


@registration_router.message(RegistrationEmplState.is_employee)
async def empl_full_name_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    full_name = message.text

    if is_valid_name(full_name):
        full_name = full_name.split()
        update_employer(tg_id, {"last_name": full_name[0],
                                "first_name": full_name[1],
                                "patronymic": full_name[2]})

        await state.set_state(RegistrationEmplState.full_name)
        message_text = 'Теперь укажите ваш номер телефона, для этого нажмите на кнопку "Поделиться номером" ниже.'
        await message.answer(message_text, reply_markup=share_phone_number_markup)
    else:
        await message.answer("Некорретные данные.\n"
                             "Укажите ваши фамилию, имя и отчество в следующем формате: <i>Иванов Иван Иванович</i>",
                             parse_mode=enums.ParseMode.HTML)



async def send_verification_request(unverified_user_tg_id: int, bot):
    user = get_user(unverified_user_tg_id)
    message_text = (f"Новая заявка на верификацию:\n\n"
                    f"ФИО: {user.last_name} {user.first_name} {user.patronymic}\n"
                    f"Номер телефона: {user.phone_number}\n"
                    f"Email: {user.email}\n"
                    f"Адрес: {user.address}\n"
                    f"Квартира: {user.apartment}\n"
                    f"Жилой комплекс: {user.residential_complex}")

    for empl in get_all_confirmed_employers():
        await send_message_to_empl(bot, empl.telegram_id, message_text, reply_markup=await get_verif_markup(user.telegram_id))


@registration_router.callback_query(lambda query: query.data.startswith("verif-approve-"))
async def approve_verif_request(query: types.CallbackQuery):
    tg_id = int(query.data[14:])
    user = get_user(tg_id)

    if user.is_registration_reviewed:
        await query.answer('Заявку уже рассмотрел другой сотрудник')
        if user.is_confirmed:
            new_text = '\n\n✅ Уже подтверждена другим сотрудником'
        else:
            new_text = '\n\n❌ Уже отклонена другим сотрудником'
        await query.bot.edit_message_text(query.message.text + new_text,
                                          query.message.chat.id, query.message.message_id)
    else:
        update_user(tg_id, {"is_confirmed": True, "is_registration_reviewed": True})
        await query.bot.send_message(tg_id, "Ваша заявка на регистрацию подтверждена", reply_markup=main_menu_markup)

        await query.bot.edit_message_text(query.message.text + '\n\n✅ Подтверждена',
                                          query.message.chat.id, query.message.message_id)


@registration_router.callback_query(lambda query: query.data.startswith('verif-reject-'))
async def reject_verif_request(query: types.CallbackQuery):
    tg_id = int(query.data[13:])

    user = get_user(tg_id)
    if user.is_registration_reviewed:
        await query.answer('Заявку уже рассмотрел другой сотрудник')
        if user.is_confirmed:
            new_text = '\n\n✅ Уже подтверждена другим сотрудником'
        else:
            new_text = '\n\n❌ Уже отклонена другим сотрудником'
        await query.bot.edit_message_text(query.message.text + new_text,
                                          query.message.chat.id, query.message.message_id)
    else:
        await query.bot.send_message(tg_id, "Ваша заявка на регистрацию отклонена.\nДля изменения данных: /start")
        delete_user_by_id(tg_id)

        await query.bot.edit_message_text(query.message.text + '\n\n❌ Отклонена',
                                          query.message.chat.id, query.message.message_id)


@registration_router.message(RegistrationState.address)
async def apartment_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id

    try:
        apartment = int(message.text)       # ValueError возникнет, если не получится перевести в int
        if apartment <= 0:                  # или если номер квартиры <= 0
            raise ValueError
    except ValueError:
        await message.answer("Некорретные данные.\nВведите номер вашей квартиры.")
        return

    update_user(tg_id, {"apartment": apartment})

    all_complexes = get_all_residentials()

    buttons = [
        [KeyboardButton(text=complex.name)]
        for complex in all_complexes
    ]
    complex_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await state.set_state(RegistrationState.apartment)
    await message.answer("Теперь выберете ваш жилой комплекс.", reply_markup=complex_markup)


@registration_router.message(RegistrationState.apartment)
async def residential_complex_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    username = message.from_user.username
    residential_complex = message.text

    if residential_complex in [complex.name for complex in get_all_residentials()]:
        residential_complex_id = get_residential_id_by_name(residential_complex)

        if residential_complex_id:
            update_user(tg_id, {
                                    'residential_complex_id':residential_complex_id,
                                    'username': username,
                                    'tg_link': 'https://t.me/' + username,
                                })
            await state.clear()

            await send_verification_request(tg_id, message.bot)
            await message.answer("Регистрация завершена. Данные отправлены на верификацию сотруднику управляющей компании")

    else: 
        all_complexes = get_all_residentials()
        buttons = [
            [KeyboardButton(text=complex.name)]
            for complex in all_complexes
        ]
        complex_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await state.set_state(RegistrationState.apartment)
        await message.answer("Вы выбрали неверный ЖК, повторите попытку!", reply_markup=complex_markup)

    
@registration_router.message(RegistrationState.email)
async def address_selected(message: types.Message, state: FSMContext):
    address = message.text
    tg_id = message.from_user.id

    if len(address) > 5:
        update_user(tg_id, {"address": address})
        await state.set_state(RegistrationState.address)
        await message.answer('Теперь введите номер квартиры:')
    else:
        await message.answer('Некорректный адрес.\n\nУкажите ваш адрес. Пример: <i>Попова, 13</i>',
                             parse_mode=enums.ParseMode.HTML)


@registration_router.message(RegistrationState.phone_number)
async def email_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    email = message.text

    if is_valid_email(email):
        update_user(tg_id, {"email": email})
        await state.set_state(RegistrationState.email)
        await message.answer('Укажите ваш адрес. Пример: <i>Попова, 13</i>',
                             parse_mode=enums.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Некорретный адрес.\nВведите ваш адрес электронной почты.")


@registration_router.message(RegistrationState.full_name)
async def phone_number_selected(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id

    # если отправили чужой контакт или сообщение не того типа
    if not hasattr(message.contact, 'phone_number') or message.contact.user_id != message.from_user.id:
        await message.answer('Некорретный ввод. Кнопка ниже')
        return

    update_user(tg_id, {"phone_number": message.contact.phone_number})
    await state.set_state(RegistrationState.phone_number)
    await message.answer('Введите ваш адрес электронной почты.')


@registration_router.message(RegistrationState.role)
async def full_name_selected(message: types.Message, state: FSMContext):
    full_name = message.text

    if is_valid_name(full_name):
        full_name = full_name.split()
        update_user(message.from_user.id, {"last_name": full_name[0],
                                           "first_name": full_name[1],
                                           "patronymic": full_name[2]})

        await state.set_state(RegistrationState.full_name)
        message_text = 'Теперь укажите ваш номер телефона, для этого нажмите на кнопку "Поделиться номером" ниже.'
        await message.answer(message_text, reply_markup=share_phone_number_markup)
    else:
        await message.answer("Некорретные данные.\n"
                             "Укажите ваши фамилию, имя и отчество в следующем формате: <i>Иванов Иван Иванович</i>",
                             parse_mode=enums.ParseMode.HTML)


@registration_router.callback_query(lambda query: query.data in role_texts.keys())
async def role_selected(query: types.CallbackQuery, state: FSMContext):
    role = role_texts.get(query.data)
    tg_id = query.from_user.id

    if role == 'Житель':
        create_user(tg_id, delete_if_exists=True)
        await state.set_state(RegistrationState.role)
    elif role == 'Сотрудник УК':
        create_employer(tg_id, delete_if_exists=True)
        await state.set_state(RegistrationEmplState.is_employee)

    message_text = (
        f'Вы выбрали роль: {role}\n\n'
        'Теперь укажите ваши фамилию, имя и отчество в следующем формате: <i>Иванов Иван Иванович</i>'
    )
    await query.message.answer(message_text, parse_mode=enums.ParseMode.HTML)
    await query.answer()


async def send_message_to_empl(bot, tg_id: int, message_text: str, reply_markup=None):
    """Отправляет сообщение, ловит исключения"""
    try:
        await bot.send_message(tg_id, message_text, reply_markup=reply_markup)
    except exceptions.TelegramForbiddenError:
        logger.error(f'Сотрудник {tg_id} заблокировал бота')
    except exceptions.TelegramBadRequest:
        logger.error(f'Чат с сотрудником {tg_id} не существует')
