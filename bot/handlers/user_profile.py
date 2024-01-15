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
                f"Жилой комплекс: {user.residential_complex}\n"
                f"Номер телефона: {user.phone_number}\n"
                f"Email: {user.email}\n"
                f"Роль: {user.role.role}\n"
                f"Подтвержден: {user.is_confirmed}"
            )
            return profile
        else:
            return None
    except Exception as e:
        print(str(e)) # В логи пихать, не принт
