import functools
from db.db_config import *

def get_user(tg_id: int) -> User:
    try:
        User.set_session(Session())
        return User.get_user_by_id(tg_id)
    finally:
        User.close_session()

def update_user_by_id(tg_id: int, updated_data:dict) -> None:
    try:
        User.set_session(Session())
        User.update_user_by_id(tg_id, updated_data)
    finally:
        User.close_session()

def delete_user_by_id(tg_id: int) -> None:
    try:
        User.set_session(Session())
        User.delete_user_by_id(tg_id)
    finally:
        User.close_session()

def get_all_tickets() -> list[Ticket]:
    try:
        Ticket.set_session(Session())
        return Ticket.get_all()
    finally:
        Ticket.close_session()

def get_solved_tickets() -> list[Ticket]:
    try:
        Ticket.set_session(Session())
        return Ticket.get_solved()
    finally:
        Ticket.close_session()

def get_unsolved_tickets() -> list[Ticket]:
    try:
        Ticket.set_session(Session())
        return Ticket.get_unsolved()
    finally:
        Ticket.close_session()

def get_all_news() -> list[News]:
    try:
        News.set_session(Session())
        return News.get_all()
    finally:
        News.close_session()

def get_news_by_id(news_id: int) -> News:
    try:
        News.set_session(Session())
        return News.get_by_id(news_id)
    finally:
        News.close_session()

def delete_news_by_id(news_id: int) -> News:
    try:
        News.set_session(Session())
        return News.delete_by_id(news_id)
    finally:
        News.close_session()

def get_ticket_by_id(ticket_id: int) -> Ticket:
    try:
        Ticket.set_session(Session())
        return Ticket.get_by_id(ticket_id)
    finally:
        Ticket.close_session()

def get_ticket_type_by_id(ticket_type_id: int) -> Ticket:
    try:
        TicketType.set_session(Session())
        return TicketType.get_by_id(ticket_type_id)
    finally:
        TicketType.close_session()

def get_employer_by_id(employer_id: int) -> Employer:
    try:
        Employer.set_session(Session())
        return Employer.get_by_id(employer_id)
    finally:
        Employer.close_session()

def get_all_employers_ids():
    try:
        Employer.set_session(session)
        return Employer.get_all_telegram_ids()
    finally:
        Employer.close_session()

def get_all_users_by_complex_id(complex_id):
    try:
        User.set_session(Session())
        return User.get_all_by_complex_id(complex_id)
    finally:
        User.close_session()


def get_all_users_ids():
    try:
        User.set_session(Session())
        return User.get_all_telegram_ids()
    finally:
        User.close_session()

def get_all_users():
    try:
        User.set_session(Session())
        return User.get_all()
    finally:
        User.close_session()

def get_all_confirmed_users() -> list[User]:
    try:
        User.set_session(Session())
        return User.get_all_confirmed_users()
    finally:
        User.close_session()

def create_ticket(new_ticket: Ticket) -> None:
    try:
        Ticket.set_session(Session())
        Ticket.create_ticket(new_ticket)
    finally:
        Ticket.close_session()

def create_poll(poll_data: Poll) -> None:
    try:
        Poll.set_session(Session())
        Poll.create_poll(poll_data)
    finally:
        Poll.close_session()

def get_all_polls() -> list[Poll]:
    try:
        Poll.set_session(Session())
        return Poll.get_all()
    finally:
        Poll.close_session()

def get_all_active_polls(user_id) -> list[Poll]:
    try:
        Poll.set_session(Session())
        return Poll.get_all_active(user_id)
    finally:
        Poll.close_session()

def get_all_inactive_polls(user_id) -> list[Poll]:
    try:
        Poll.set_session(Session())
        return Poll.get_all_inactive(user_id)
    finally:
        Poll.close_session()

def get_poll_by_id(poll_id) -> Poll:
    try:
        Poll.set_session(Session())
        return Poll.get_by_id(poll_id)
    finally:
        Poll.close_session()

def delete_poll_by_id(poll_id) -> Poll:
    try:
        Poll.set_session(Session())
        return Poll.delete_by_id(poll_id)
    finally:
        Poll.close_session()

def close_pole(poll_id) -> None:
    try:
        Poll.set_session(Session())
        Poll.delete_by_id(poll_id)
    finally:
        Poll.close_session()

def get_id_by_ticket_type_name(problem_type_name: String) -> int:
    try:
        TicketType.set_session(Session())
        return TicketType.get_id_by_ticket_type_name(problem_type_name)
    finally:
        TicketType.close_session()


def get_all_by_user_id_and_status(tg_id:int, is_solved:int) -> list[Ticket]:
    try:
        Ticket.set_session(Session())
        return Ticket.get_all_by_user_id_and_status(tg_id, is_solved)
    finally:
        Ticket.close_session()


def create_new_news(news_data: News) -> None:
    try:
        News.set_session(Session())
        News.create_news(news_data)
    finally:
        News.close_session()

def update_user(tg_id: int, updated_data: dict) -> None:
    try:
        User.set_session(Session())
        User.get_user_by_id(tg_id).update(updated_data)
    finally:
        User.close_session()


def update_employer(tg_id: int, updated_data: dict) -> None:
    try:
        Employer.set_session(Session())
        Employer.update_by_id(tg_id, updated_data)
    finally:
        Employer.close_session()


def get_all_confirmed_employers() -> list[Employer]:
    try:
        Employer.set_session(Session())
        return Employer.get_all_confirmed_employers()
    finally:
        Employer.close_session()

def get_all_confirmed_employees_with_role(role_name: str) -> list[Employer]:
    Employer.set_session(Session())
    confirmed_empls = []
    for empl in Employer.get_all_by_role(role_name):
        if empl.is_confirmed:
            confirmed_empls.append(empl)
    Employer.close_session()
    return confirmed_empls


def create_user(tg_id: int, delete_if_exists=False) -> None:
    session = Session()
    User.set_session(session)
    UserRole.set_session(session)
    role_id: int = UserRole.get_role_id_by_role_name('Собственник')

    if delete_if_exists and User.exists(tg_id):
        User.delete_user_by_id(tg_id)

    new_user_data = {
        "telegram_id": tg_id,
        "role_id": role_id,
        "is_confirmed": False,
        "is_registration_reviewed": False
    }
    new_user = User(**new_user_data)
    new_user.save()
    User.close_session()
    UserRole.close_session()

def get_user_by_id(tg_id: int) -> User:
    session = Session()
    try:
        return session.get(User, tg_id)
    finally:
        User.close_session()

def get_employer_by_id(tg_id: int) -> User:
    session = Session()
    try:
        return session.get(Employer, tg_id)
    finally:
        Employer.close_session()

def create_employer(tg_id: int, delete_if_exists=False) -> None:
    session = Session()
    Employer.set_session(session)
    EmployerRole.set_session(session)

    if delete_if_exists and Employer.exists(tg_id):
        Employer.delete_by_id(tg_id)

    new_empl_data = {
        "telegram_id": tg_id,
        "is_confirmed": False,
        "is_registration_reviewed": False
    }
    new_empl = Employer(**new_empl_data)
    new_empl.save()

    Employer.close_session()
    EmployerRole.close_session()

def get_employer_role_id_by_role_name(role_name: str) -> int:
    try:
        EmployerRole.set_session(session)
        return EmployerRole.get_role_id_by_role_name(role_name)
    finally:
        EmployerRole.close_session()


def get_employer_role_by_id(role_id: int) -> EmployerRole:
    try:
        EmployerRole.set_session(Session())
        return EmployerRole.get_by_id(role_id)
    finally:
        EmployerRole.close_session()

def ban_user_by_id(tg_id: int) -> Boolean:
    try:
        User.set_session(Session())
        User.ban(tg_id)
        return True
    except Exception:
        return False
    finally:
        User.close_session()

def close_ticket_by_id(ticket_id: int) -> Boolean:
    try:
        Ticket.set_session(Session())
        Ticket.close_ticket(ticket_id)
        return True
    except Exception:
        return False
    finally:
        Ticket.close_session()
    

def delete_ticket_by_id(ticket_id: int) -> Boolean:
    try:
        Ticket.set_session(Session())
        Ticket.delete_ticket(ticket_id)
        return True
    except Exception:
        return False
    finally:
        Ticket.close_session()


def get_all_residentials() -> list[ResidentialComplex]:
    try:
        ResidentialComplex.set_session(Session())
        all_complexes = ResidentialComplex.get_all()
        return all_complexes
    except Exception:
        return None
    finally:
        ResidentialComplex.close_session()

def get_residential_id_by_name(residential_complex_name) -> int:
    try:
        ResidentialComplex.set_session(Session())
        complex_id = ResidentialComplex.get_id_by_name(residential_complex_name)
        return complex_id
    except Exception:
        return None
    finally:
        ResidentialComplex.close_session()