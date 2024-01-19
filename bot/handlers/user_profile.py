from utils.db_requests import get_user_by_id


async def user_profile_handler(user_id):
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
        print(str(e)) # В логи пихать, не принт
