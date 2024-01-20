from utils.db_requests import get_user_by_id, get_employer_by_id


async def user_profile_handler(user_id, logger):
    try:
        user = get_user_by_id(user_id)
        if user:
            profile = (
                f"Имя: {user.first_name}\n"
                f"Фамилия: {user.last_name}\n"
                f"Отчество: {user.patronymic}\n"
                f"Адрес: {user.address}\n"
                f"Квартира: {user.apartment}\n"
                f"Жилой комплекс: {user.residential_complex.name}\n"
                f"Номер телефона: {user.phone_number}\n"
                f"Email: {user.email}\n"
                f"Роль: {user.role.role}\n"
                f"Подтвержден: {'Да' if user.is_confirmed else 'Нет'}"
            )
            return profile
        else:
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении профиля юзера: {str(e)}")


async def user_profile_for_employer_handler(user_id, logger):
    try:
        user = get_user_by_id(user_id)
        if user:
            profile = (
                f"Имя: {user.first_name}\n"
                f"Фамилия: {user.last_name}\n"
                f"Отчество: {user.patronymic}\n"
                f"Адрес: {user.address}\n"
                f"Квартира: {user.apartment}\n"
                f"Жилой комплекс: {user.residential_complex.name}\n"
                f"Номер телефона: {user.phone_number}\n"
                f"Контакт: @{user.username}\n"
                f"Связаться: {user.tg_link}\n"
                f"Email: {user.email}\n"
                f"Роль: {user.role.role}\n"
                f"Подтвержден: {'Да' if user.is_confirmed else 'Нет'}"
            )
            return profile
        else:
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении профиля юзера: {str(e)}")

async def employer_profile_handler(employer_id, logger):
    try:
        employer = get_employer_by_id(employer_id)
        if employer:
            profile = (
                f"Имя: {employer.first_name}\n"
                f"Фамилия: {employer.last_name}\n"
                f"Отчество: {employer.patronymic}\n"
                f"Жилой комплекс: {employer.residential_complex.name}\n"
                f"Номер телефона: {employer.phone_number}\n"
                f"Email: {employer.email}\n"
                f"Роль: {employer.role.role}\n"
                f"Подтвержден: {'Да' if employer.is_confirmed else 'Нет'}"
            )
            return profile
        else:
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении профиля работника: {str(e)}")