from sqlalchemy import create_engine, DateTime, TIMESTAMP, Column, Integer, String, Boolean, ForeignKey, Date, text, Time, Text, BigInteger, JSON as Json, DECIMAL
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.exc import NoResultFound
import datetime
import logging



Base = declarative_base()

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

file_handler = logging.FileHandler('db/logs/DB_logs.log', encoding='utf-8')
# file_handler = logging.FileHandler('logs/DB_logs.log', encoding='utf-8')
file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)

def delete_old_log_entries(log_file_path, days_to_keep=7):
    from datetime import datetime, timedelta
    current_datetime = datetime.now()

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    filtered_lines = []

    for line in lines:
        parts = line.split()

        if len(parts) >= 3:
            date_str = f'{parts[0]} {parts[1]}'
            try:
                log_datetime = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
            except ValueError:
                continue

            if current_datetime - log_datetime < timedelta(days=days_to_keep):
                filtered_lines.append(line)

    with open(log_file_path, 'w') as log_file:
        log_file.writelines(filtered_lines)

log_file_path = 'my_log.log'
# delete_old_log_entries(log_file_path, 7)

# class BaseClass(Base):
#     pass

class User(Base):
    __tablename__ = 'user'
    telegram_id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String)
    tg_link = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    apartment = Column(String)
    residential_complex_id = Column(Integer)
    phone_number = Column(String)
    address = Column(String)
    email = Column(String)
    image = Column(String)
    is_confirmed = Column(Boolean)
    is_registration_reviewed = Column(Boolean)
    is_active = Column(Boolean, default=1)
    is_banned = Column(Boolean, default=0)
    
    # Определите внешние ключи
    role_id = Column(Integer, ForeignKey('user_role.role_id'))
    residential_complex_id = Column(Integer, ForeignKey('residential_complex.residential_complex_id'))

    # Определите связи
    role = relationship('UserRole')
    residential_complex = relationship('ResidentialComplex')

    _session = None  
    def __init__(self, **user_data):
        logger.info(f"Создание юзера с данными: {user_data}")
        try:
            super().__init__(**user_data)
        except Exception as e:
            logger.error(f"Ошибка при создании юзера: {str(e)}")

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

          
    @classmethod
    def get_all(cls):
        all_users = cls.get_session().query(cls).all()
        return all_users

    @classmethod
    def get_user_by_id(cls, telegram_id):
        session = cls.get_session()
        try:
            user = session.get(cls, telegram_id)
            if not user:
                return None
            return user
        except Exception as e:
            logger.error("Ошибка при получении пользователя по id: ", str(e))
            return None

    @classmethod
    def get_all_unconfirmed_users(cls):
        logger.info(f"Запрос всех неподтвержденных пользователей")
        try:
            query = text(f"SELECT * FROM resident_bot_db.user WHERE is_confirmed = 0")
            all_unconfirmed_users = cls.get_session().execute(query).fetchall()
            if all_unconfirmed_users:
                return all_unconfirmed_users
            return None 
            # all_unconfirmed_users = cls.get_session().query(cls).filter_by(is_confirmed=False)
            # return all_unconfirmed_users
        except Exception:
            logger.error("Ошибка при всех неподтвержденных пользователей: ", str(Exception))
            return None
    
    @classmethod
    def get_all_confirmed_users(cls):
        logger.info(f"Запрос всех подтвержденных пользователей")
        try:
            query = text(f"SELECT telegram_id FROM resident_bot_db.user WHERE is_confirmed = 1")
            all_confirmed_users = cls.get_session().execute(query).fetchall()
            if all_confirmed_users:
                return all_confirmed_users
            return None 
        except Exception:
            logger.error("Ошибка при всех подтвержденных пользователей: ", str(Exception))
            return None

    @classmethod
    def get_all_telegram_ids(cls):
        logger.info(f"Запрос всех id пользователей")
        all_users = cls.get_session().query(cls).all()
        telegram_ids = [user.telegram_id for user in all_users]
        return telegram_ids
    
    @classmethod
    def get_all_by_complex_id(cls, complex_id):
        all_users_by_complex = cls.get_session().query(cls).filter_by(residential_complex_id=complex_id)
        return all_users_by_complex
    
    @classmethod
    def confirm_user_by_id(cls, telegram_id):
        logger.info(f"Запрос на подтверждение пользователя по id")
        try:
            user = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one()
            if not user:
                return False
            else:
                user.is_confirmed = True
                cls.get_session().commit()
                return True
        except Exception:
            logger.error("Ошибка при неподтверждении пользователя: ", str(Exception))
            print("Ошибка при неподтверждении пользователя: ", str(Exception))
            return False

    @classmethod
    def create_user(cls, user_data):
        logger.info(f"Запрос на создание нового пользователя")
        try:
            new_user = cls(**user_data)
            cls.get_session().add(new_user)
            cls.get_session().commit()
            return new_user
        except Exception:
            logger.error(f"Ошибка при создании пользователя: с telegram_id={new_user.telegram_id} ", str(Exception))
            return None

    @classmethod
    def delete_user_by_id(cls, telegram_id):
        logger.info(f"Запрос на удаление пользователя по id")
        try:
            session = cls.get_session()
            user = session.get(cls, telegram_id)
            if user:
                session.delete(user)
                session.commit()
                return True
            else:
                return False
        except Exception:
            logger.error("Ошибка при удалении пользователя: ", str(Exception))
            return None

    @classmethod
    def update_user_by_id(cls, telegram_id, updated_data):
        logger.info(f"Запрос на обновление пользователя по id")
        try:
            user = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one()
            for key, value in updated_data.items():
                setattr(user, key, value)
            cls.get_session().commit()
            return True
        except Exception:
            logger.error("Ошибка при обновлении пользователя: ", str(Exception))
            return None


    @classmethod
    def ban(cls, telegram_id):
        try:
            session = cls.get_session()
            user = session.query(cls).filter_by(telegram_id=telegram_id).one_or_none()

            if user:
                user.is_banned = 1
                session.commit()  
                return True
            else:
                return False
        except Exception as e:
            logger.error("Ошибка при бане пользователя: " + str(e))
            return False
        finally:
            session.close()  
    
    @classmethod
    def unban(cls, telegram_id):
        try:
            session = cls.get_session()
            user = session.query(cls).filter_by(telegram_id=telegram_id).one_or_none()

            if user:
                user.is_banned = 0
                session.commit()  
                return True
            else:
                return False
        except Exception as e:
            logger.error("Ошибка при бане пользователя: " + str(e))
            return False
        finally:
            session.close()  

    @classmethod
    def exists(cls, telegram_id):
        logger.info("Запрос на проверку существования пользователя по id")
        try:
            user = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one_or_none()
            if user is not None:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Ошибка при проверке существования пользователя: " + str(e))
            return None

    def save(self):
        logger.info(f"Запрос на сохренение нового пользователя")
        try:
            self._session.add(self)
            self._session.commit()
        except Exception as e:
            logger.error("Ошибка при сохранении пользователя: ", str(e))
            return None

    def update(self, updated_data):
        session = self.__class__.get_session()
        try:
            user = session.get(User, self.telegram_id)
            if user:
                for key, value in updated_data.items():
                    setattr(user, key, value)
                session.commit()
                return True
            else:
                return False
        except Exception:
            logger.error("Ошибка при обновлении пользователя: ", str(Exception))
            return None
        
    def delete(self):
        session = self.get_session()
        try:
            user = session.get(User, self.telegram_id)
            if user:
                session.delete(user)
                session.commit()
                return True
            else:
                return False
        except Exception:
            logger.error("Ошибка при удалении пользователя: ", str(Exception))
            return None

    @classmethod
    def close_session(self):
        if self._session:
            self._session.close()

class UserRole(Base):
    __tablename__ = 'user_role'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String)


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session
    
    @classmethod
    def get_all(cls):
        try:
            session = cls.get_session()
            roles = session.query(cls).all()
            return roles
        except Exception as e:
            logger.error(f"Не удалось получить все роли: {str(e)}")
            return []

    @classmethod
    def get_by_id(cls, role_id):
        try:
            session = cls.get_session()
            role = session.get(cls, role_id)
            return role
        except Exception as e:
            logger.error(f"Не удалось получить роль по ID: {str(e)}")
            return None

    @classmethod
    def get_role_id_by_role_name(cls, role_name):
        logger.info(f"Запрос id роли пользователя по имени роли")
        try:
            sql = text(f"SELECT role_id FROM resident_bot_db.user_role WHERE role = '{role_name}'")
            role = cls.get_session().execute(sql, {"role_name": role_name}).fetchone()
            if role:
                return role[0] 
            return None 
        except Exception as e:
            logger.error(f"Не удалось получить ID роли по её имени: {str(e)}")
            return None

    @classmethod
    def create_role(cls, role_name):
        try:
            role = cls(role=role_name)
            session = cls.get_session()
            session.add(role)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Не удалось создать роль: {str(e)}")
            return False

    def save(self):
        try:
            session = self._session
            session.add(self)
            session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить роль: {str(e)}")

    @classmethod
    def update_role_by_id(cls, role_id, new_role_name):
        try:
            role = cls.get_by_id(role_id)
            if role:
                role.role = new_role_name
                cls.get_session().commit()
                return role
            else:
                return None
        except Exception as e:
            logger.error(f"Не удалось обновить роль по ID: {str(e)}")
            return None

    @classmethod
    def delete_role_by_id(cls, role_id):
        try:
            role = cls.get_by_id(role_id)
            if role:
                session = cls.get_session()
                session.delete(role)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Не удалось удалить роль по ID: {str(e)}")
            return False

    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")
    

class Employer(Base):
    __tablename__ = 'employer'
    telegram_id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    email = Column(String)
    is_confirmed = Column(Boolean)
    is_registration_reviewed = Column(Boolean)
    
    # Определите внешний ключ
    role_id = Column(BigInteger, ForeignKey('employer_role.role_id'))
    residential_complex_id = Column(BigInteger, ForeignKey('residential_complex.residential_complex_id'))
    # Определите связь с таблицей employer_role
    role = relationship('EmployerRole')
    residential_complex = relationship('ResidentialComplex')

    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all_by_role(cls, role_name):
        try:
            query = text(f"""SELECT * FROM resident_bot_db.employer 
                         JOIN employer_role ON employer.role_id = employer_role.role_id 
                         WHERE employer_role.role = '{role_name}'""")
            employers_with_role = cls.get_session().execute(query).fetchall()

            return employers_with_role
        except Exception as e:
            logger.error(f"Не удалось получить работодателей с ролью {role_name}: {str(e)}")
            return None
        
    @classmethod
    def get_all(cls):
        try:
            session = cls.get_session()
            roles = session.query(cls).all()
            return roles
        except Exception as e:
            logger.error(f"Не удалось получить всех работодателей: {str(e)}")
            return None

    @classmethod
    def get_all_telegram_ids(cls):
        try:
            all_employers = cls.get_session().query(cls).all()
            telegram_ids = [employer.telegram_id for employer in all_employers]
            return telegram_ids
        except Exception as e:
            logger.error(f"Не удалось получить все Telegram ID: {str(e)}")
            return None

    @classmethod
    def delete_by_id(cls, telegram_id):
        try:
            employer = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one()
            cls.get_session().delete(employer)
            cls.get_session().commit()
            return True
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить работодателя по Telegram ID: {str(e)}")
            return False

    @classmethod
    def get_by_id(cls, telegram_id):
        try:
            sql = text(f"SELECT * FROM resident_bot_db.employer WHERE telegram_id = '{telegram_id}'")
            employer = cls.get_session().execute(sql, {"telegram_id": telegram_id}).fetchone()
            if employer:
                return employer
            return None
        except Exception as e:
            logger.error(f"Не удалось получить работодателя по Telegram ID: {str(e)}")
            return None

    @classmethod
    def update_by_id(cls, telegram_id, updated_data):
        try:
            logger.info(f"Запрос на обновление данных о работнике с id={telegram_id}")
            employer = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one()
            if employer:
                for key, value in updated_data.items():
                    setattr(employer, key, value)
                employer.save()
                return True
            else:
                logger.error(f"Работодатель с Telegram ID: {str(e)} не найден")
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить работодателя по Telegram ID: {str(e)}")

    @classmethod
    def create_employer(cls, employer_data):
        new_employer = cls(**employer_data)
        cls.get_session().add(new_employer)
        cls.get_session().commit()
        return new_employer

    @classmethod
    def get_all_confirmed_employers(cls):
        logger.info(f"Запрос всех подтвержденных сотрудников")
        try:
            query = text(f"SELECT * FROM resident_bot_db.employer WHERE is_confirmed = 1")
            all_confirmed_employers = cls.get_session().execute(query).fetchall()
            if all_confirmed_employers:
                return all_confirmed_employers
            return None 
        except Exception:
            logger.error("Ошибка при всех подтвержденных сотрудников: ", str(Exception))
            return None

    @classmethod
    def exists(cls, telegram_id):
        logger.info("Запрос на проверку существования работника по id")
        try:
            user = cls.get_session().query(cls).filter_by(telegram_id=telegram_id).one_or_none()
            if user is not None:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Ошибка при проверке существования работника: " + str(e))
            return None
        
    def save(self):
        try:
            self._session.add(self)
            self._session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить работодателя: {str(e)}")

    def delete(self):
        session = self.get_session()
        try:
            employer = session.query(Employer).get(telegram_id=self.telegram_id)
            if employer:
                session.delete(employer)
                session.commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить работодателя: {str(e)}")

    def update(self, updated_data):
        session = self.get_session()
        try:
            employer = session.query(Employer).filter_by(telegram_id=self.telegram_id).one()
            for key, value in updated_data.items():
                setattr(employer, key, value)
            session.commit()
            return True
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить работодателя: {str(e)}")
            return False
   
    @classmethod
    def close_session(self):
        if self._session:
            self._session.close()
        

class EmployerRole(Base):
    __tablename__ = 'employer_role'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String)

    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            session = cls.get_session()
            roles = session.query(cls).all()
            return roles
        except Exception as e:
            logger.error(f"Не удалось получить все роли работодателей: {str(e)}")

    @classmethod
    def get_by_id(cls, role_id):
        return cls.get_session().get(cls, role_id)
    
    @classmethod
    def get_role_id_by_role_name(cls, role_name):
        try:
            sql = text(f"SELECT role_id FROM resident_bot_db.employer_role WHERE role = '{role_name}'")
            role = cls.get_session().execute(sql, {"role_name": role_name}).fetchone()
            if role:
                return role[0] 
            return None 
        except Exception as e:
            logger.error(f"Не удалось получить ID роли по её имени: {str(e)}")
            return None

    @classmethod
    def create_role(cls, role_name):
        try:
            role = cls(role=role_name)
            session = cls.get_session()
            session.add(role)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Не удалось создать роль: {str(e)}")

    @classmethod
    def update_role_by_id(cls, role_id, new_role_name):
        try:
            session = cls.get_session()
            role = cls.get_role_by_id(session, role_id)
            if role:
                role.role = new_role_name
                session.commit()
                return role
            else:
                return None
        except Exception as e:
            logger.error(f"Не удалось обновить роль по ID: {str(e)}")

    @classmethod
    def delete_role_by_id(cls, role_id):
        try:
            session = cls.get_session()
            role = cls.get_role_by_id(session, role_id)
            if role:
                session.delete(role)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить роль по ID: {str(e)}")

    def save(self):
        try:
            session = self._session
            session.add(self)
            session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить роль: {str(e)}")

    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")

class Ticket(Base):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.telegram_id'))
    ticket_type_id = Column(Integer, ForeignKey('ticket_type.ticket_type_id'))
    date = Column(Date)
    time = Column(Time)
    details = Column(String)
    is_solved = Column(Boolean)
    images = Column(String)
    # Определите связи с другими таблицами
    user = relationship('User')
    ticket_type = relationship('TicketType')


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            logger.info(f"Запрос на получение всех заявок")
            query = text(f"""
                          SELECT 
                                ticket.ticket_id,
                                ticket_type.type,
                                ticket.user_id,
                                ticket.is_solved,
                                ticket.date,
                                ticket.time,
                                ticket.details,
                                ticket.images
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                            ORDER BY date DESC
                         """)
            all_tickets = cls.get_session().execute(query).fetchall()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить все билеты: {str(e)}")

    @classmethod
    def get_all_by_user_id(cls, telegram_id:int):
        try:
            sql = text(f"""
                          SELECT 
                                ticket.*,
                                ticket_type.type
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                            WHERE
                                user_id = {telegram_id}
                         """)
            all_tickets = cls.get_session().execute(sql).fetchall()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить все заявки: {str(e)}")

    @classmethod
    def get_solved(cls):
        try:
            logger.info(f"Запрос на получение всех закрытых заявок")
            query = text(f"""
                          SELECT 
                                ticket.ticket_id,
                                ticket_type.type,
                                ticket.user_id,
                                ticket.is_solved,
                                ticket.date,
                                ticket.time,
                                ticket.details,
                                ticket.images
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                            WHERE
                                ticket.is_solved = 1
                         """)
            all_tickets = cls.get_session().execute(query).fetchall()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить все закрытые заявки: {str(e)}")
    
    @classmethod
    def get_unsolved(cls):
        try:
            logger.info(f"Запрос на получение всех открытых заявок")
            query = text(f"""
                          SELECT 
                                ticket.ticket_id,
                                ticket_type.type,
                                ticket.user_id,
                                ticket.is_solved,
                                ticket.date,
                                ticket.time,
                                ticket.details,
                                ticket.images
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                            WHERE
                                ticket.is_solved = 0
                         """)
            all_tickets = cls.get_session().execute(query).fetchall()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить все открытые заявки: {str(e)}")
    
    @classmethod
    def get_all_by_user_id_and_status(cls, telegram_id:int, is_solved:int):
        try:
            sql = text(f"""
                          SELECT 
                                ticket.*,
                                ticket_type.type,
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                            WHERE
                                user_id = {telegram_id} AND is_solved = {is_solved}
                         """)
            all_tickets = cls.get_session().execute(sql).fetchall()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить все заявки: {str(e)}")


    @classmethod
    def delete_by_id(cls, ticket_id):
        session = cls.get_session()
        try:
            ticket = session.query(cls).get(ticket_id)
            if ticket:
                session.delete(ticket)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить билет: {str(e)}")

    @classmethod
    def get_by_id(cls, ticket_id):
        try:
            query = text(f"""
                          SELECT 
                                ticket.ticket_id,
                                ticket_type.type,
                                ticket.user_id,
                                ticket.is_solved,
                                ticket.date,
                                ticket.time,
                                ticket.details,
                                ticket.images,
                                user.username,
                                user.telegram_id,  
                                user.tg_link  
                            FROM
                                resident_bot_db.ticket
                                    JOIN
                                resident_bot_db.ticket_type ON ticket.ticket_type_id = ticket_type.ticket_type_id
                                    JOIN
                                resident_bot_db.user ON ticket.user_id = user.telegram_id
                            WHERE ticket_id = {ticket_id}
                         """)
            all_tickets = cls.get_session().execute(query).one()
            return all_tickets
        except Exception as e:
            logger.error(f"Не удалось получить билет по ID = {ticket_id}: {str(e)}")

    @classmethod
    def update_by_id(cls, ticket_id, updated_data):
        session = cls.get_session()
        try:
            ticket = session.query(cls).filter_by(ticket_id=ticket_id).one()
            for key, value in updated_data.items():
                setattr(ticket, key, value)
            session.commit()
            return True
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить билет по ID: {str(e)}")

    @classmethod
    def close_ticket(cls, ticket_id):
        try:
            session = cls.get_session()
            ticket = session.query(cls).filter_by(ticket_id=ticket_id).one_or_none()

            if ticket:
                ticket.is_solved = 1
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Не удалось закрыть заявку с id = {ticket_id}: {str(e)}")

    @classmethod
    def delete_ticket(cls, ticket_id):
        try:
            session = cls.get_session()
            ticket = session.query(cls).filter_by(ticket_id=ticket_id).one_or_none()

            if ticket:
                ticket.delete()
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Не удалось удалить заявку с id = {ticket_id}: {str(e)}")

    @classmethod
    def create_ticket(cls, ticket_data):
        session = cls.get_session()
        if ticket_data["images"] == []:
            ticket_data["images"] = None
        new_ticket = cls(**ticket_data)
        session.add(new_ticket)
        try:
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Не удалось создать заявку: {str(e)}")
            return False

    def delete(self):
        session = self.get_session()
        try:
            ticket = session.query(Ticket).get(self.ticket_id)
            if ticket:
                session.delete(ticket)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить заявку: {str(e)}")
            return False

    def update(self, updated_data):
        session = self.get_session()
        try:
            ticket = session.query(Ticket).filter_by(ticket_id=self.ticket_id).one()
            for key, value in updated_data.items():
                setattr(ticket, key, value)
            session.commit()
            return True
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить заявку: {str(e)}")
            return False

    def save(self):
        user = User.get_user_by_id(self.user_id)
        ticket_type = TicketType.get_ticket_type_by_id(self.ticket_type_id)

        if user and ticket_type:
            self.user = user
            self.ticket_type = ticket_type
            session = self.get_session()
            session.add(self)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Не удалось сохранить заявку: {str(e)}")

    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class TicketType(Base):
    __tablename__ = 'ticket_type'
    ticket_type_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_by_id(cls, ticket_type_id):
        try:
            return cls.get_session().get(cls, ticket_type_id)
        except Exception as e:
            logger.error(f"Не удалось получить тип билета по ID: {str(e)}")

    @classmethod
    def get_all(cls):
        try:
            return cls.get_session().query(cls).all()
        except Exception as e:
            logger.error(f"Не удалось получить все типы билетов: {str(e)}")

    @classmethod
    def get_id_by_ticket_type_name(cls, ticket_type):
        try:
            sql = text(f"SELECT ticket_type_id FROM resident_bot_db.ticket_type WHERE type = '{ticket_type}'")
            result = cls.get_session().execute(sql, {"ticket_type": ticket_type}).fetchone()
            if result:
                return result[0] 
            return None  
        except Exception as e:
            logger.error(f"Не удалось получить id по типу билета: {str(e)}")


    @classmethod
    def create_ticket_type(cls, type_name):
        session = cls.get_session()
        try:
            ticket_type = cls(type=type_name)
            session.add(ticket_type)
            session.commit()
            return ticket_type
        except Exception as e:
            logger.error(f"Не удалось создать тип билета: {str(e)}")

    @classmethod
    def get_ticket_type_by_id(cls, ticket_type_id):
        session = cls.get_session()
        try:
            return session.query(cls).filter(cls.ticket_type_id == ticket_type_id).first()
        except Exception as e:
            logger.error(f"Не удалось получить тип билета по ID: {str(e)}")

    @classmethod
    def update_ticket_type(cls, ticket_type_id, new_type_name):
        session = cls.get_session()
        try:
            ticket_type = cls.get_ticket_type_by_id(session, ticket_type_id)
            if ticket_type:
                ticket_type.type = new_type_name
                session.commit()
                return ticket_type
            else:
                return None
        except Exception as e:
            logger.error(f"Не удалось обновить тип билета: {str(e)}")

    @classmethod
    def delete_ticket_type(cls, ticket_type_id):
        session = cls.get_session()
        try:
            ticket_type = cls.get_ticket_type_by_id(session, ticket_type_id)
            if ticket_type:
                session.delete(ticket_type)
                session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить тип билета: {str(e)}")

    def save(self):
        try:
            self._session.add(self)
            self._session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить тип билета: {str(e)}")

    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class News(Base):
    __tablename__ = 'news'
    news_id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String)    
    date = Column(Date)
    time = Column(Time)
    body = Column(String)
    tags = Column(String)
    images = Column(Json)


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            sql = text("SELECT * FROM resident_bot_db.news ORDER BY news_id DESC")
            session = cls.get_session()
            result = session.execute(sql)
            all_news = result.fetchall()
            return all_news
        except Exception as e:
            logger.error(f"Не удалось получить все новости: {str(e)}")

    @classmethod
    def get_by_id(cls, news_id):
        try:
            session = cls.get_session()
            news = session.query(cls).filter_by(news_id=news_id).one()
            if not news:
                return None
            return news
        except Exception as e:
            logger.error(f"Не удалось получить новость по ID: {str(e)}")

    @classmethod
    def delete_by_id(cls, news_id):
        session = cls.get_session()
        try:
            news = session.query(cls).get(news_id)
            if news:
                session.delete(news)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить новость: {str(e)}")

    @classmethod
    def create_news(cls, news_data):
        session = cls.get_session()
        news_user = cls(**news_data)
        session.add(news_user)
        try:
            session.commit()
            return news_user
        except Exception as e:
            logger.error(f"Не удалось создать новость: {str(e)}")
            return None

    def delete(self):
        session = self._session
        try:
            news = session.query(News).get(self.news_id)
            if news:
                session.delete(news)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить новость: {str(e)}")
            return False

    def save(self):
        try:
            self._session.add(self)
            self._session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить новость: {str(e)}")

    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class UtilityBill(Base):
    __tablename__ = 'utility_bill'

    utility_bill_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.telegram_id'))
    date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    invoice_els_number = Column(BigInteger, nullable=True)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=True)
    description = Column(Text, nullable=True)
    is_payed = Column(Boolean, nullable=True)

    user = relationship('User')

    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            session = cls.get_session()
            all_bills = session.query(cls).all()
            return all_bills
        except Exception as e:
            logger.error(f"Не удалось получить все счета: {str(e)}")

    @classmethod
    def get_by_id(cls, bill_id):
        session = cls.get_session()
        try:
            bill = session.query(cls).get(bill_id)
            if not bill:
                return None
            return bill
        except Exception as e:
            logger.error(f"Не удалось получить счет по ID: {str(e)}")

    def save(self):
        try:
            self._session.add(self)
            self._session.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить счет: {str(e)}")

    def update(self, updated_data):
        session = self.get_session()
        try:
            bill = session.query(UtilityBill).get(self.utility_bill_id)
            if bill:
                for key, value in updated_data.items():
                    setattr(bill, key, value)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить счет: {str(e)}")
            return False

    def delete(self):
        session = self.get_session()
        try:
            bill = session.query(UtilityBill).get(self.utility_bill_id)
            if bill:
                session.delete(bill)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить счет: {str(e)}")
            return False

    def make_payed(self):
        try:
            self.is_payed = 1
            self._session.commit()
        except Exception as e:
            logger.error(f"Не удалось оплатить счет: {str(e)}")
            return False    


    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class Poll(Base):
    __tablename__ = 'poll'

    poll_tg_id = Column(BigInteger, primary_key=True, nullable=True)
    message_id = Column(BigInteger, nullable=True)
    user_id = Column(BigInteger, nullable=True)
    tittle = Column(String, nullable=True)
    is_closed = Column(Boolean, nullable=False)


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            session = cls.get_session()
            all_pols = session.query(cls).all()
            return all_pols
        except Exception as e:
            logger.error(f"Не удалось получить все опросы: {str(e)}")
            return None

    @classmethod
    def get_all_active(cls, user_id):
        try:
            session = cls.get_session()
            all_pols = session.query(cls).filter_by(is_closed=0, user_id=user_id).all()
            return all_pols
        except Exception as e:
            logger.error(f"Не удалось получить все активные опросы: {str(e)}")
            return None

    @classmethod
    def get_all_inactive(cls, user_id):
        try:
            session = cls.get_session()
            all_pols = session.query(cls).filter_by(is_closed=1, user_id=user_id).all()
            return all_pols
        except Exception as e:
            logger.error(f"Не удалось получить все завершенные опросы: {str(e)}")
            return None

    @classmethod
    def get_by_id(cls, poll_tg_id):
        try:
            sql = text(f"SELECT * FROM resident_bot_db.poll WHERE poll_tg_id = '{poll_tg_id}'")
            poll = cls.get_session().execute(sql, {"poll_tg_id": poll_tg_id}).fetchone()
            if not poll:
                return None
            return poll
        except Exception as e:
            logger.error(f"Не удалось получить опрос по ID: {str(e)}")
            return None

    def save(self):
        try:
            self._session.add(self)
            self._session.commit()
            return True
        except Exception as e:
            logger.error(f"Не удалось сохранить опрос: {str(e)}")
            return False

    def update(self, updated_data):
        session = self.get_session()
        try:
            poll = session.query(Poll).get(self.poll_id)
            if poll:
                for key, value in updated_data.items():
                    setattr(poll, key, value)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось обновить опрос: {str(e)}")
            return False

    def delete(self):
        session = self.get_session()
        try:
            poll = session.query(Poll).get(self.poll_id)
            if poll:
                session.delete(poll)
                session.commit()
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить опрос: {str(e)}")
            return False

    @classmethod
    def delete_by_id(cls, poll_tg_id):
        try:
            poll = cls.get_session().query(cls).filter_by(poll_tg_id=poll_tg_id).one()
            if poll:
                cls.get_session().delete(poll)
                cls.get_session().commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить опрос: {str(e)}")
            return False
        
    @classmethod
    def create_poll(cls, poll_data):
        logger.info(f"Запрос на создание нового опроса")
        try:
            new_poll = cls(**poll_data)
            cls.get_session().add(new_poll)
            cls.get_session().commit()
            return new_poll
        except Exception as e:
            logger.error(f"Ошибка при создании опроса: с id = ", str(e))
            return None
        
    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class ResidentialComplex(Base):
    __tablename__ = 'residential_complex'

    residential_complex_id = Column(BigInteger, primary_key=True, nullable=True)
    name = Column(String, nullable=True)


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session

    @classmethod
    def get_all(cls):
        try:
            query = text(f"SELECT residential_complex_id, name FROM resident_bot_db.residential_complex;")
            all_complexes = cls.get_session().execute(query).fetchall()
            if all_complexes:
                return all_complexes
            return None 
        except Exception as e:
            logger.error(f"Не удалось получить все жилые комплексы: {str(e)}")
            return None

    @classmethod
    def get_id_by_name(cls, name):
        try:
            sql = text(f"SELECT residential_complex_id FROM resident_bot_db.residential_complex WHERE name = '{name}'")
            complex = cls.get_session().execute(sql, {"name": name}).fetchone()
            if not complex:
                return None
            return complex.residential_complex_id
        except Exception as e:
            logger.error(f"Не удалось получить ЖК по ID: {str(e)}")
            return None
    
    @classmethod
    def get_by_id(cls, residential_complex_id):
        try:
            sql = text(f"SELECT * FROM resident_bot_db.residential_complex WHERE residential_complex_id = '{residential_complex_id}'")
            complex = cls.get_session().execute(sql, {"residential_complex_id": residential_complex_id}).fetchone()
            if not complex:
                return None
            return complex
        except Exception as e:
            logger.error(f"Не удалось получить ЖК по ID: {str(e)}")
            return None
        
    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


class MeterReading(Base):
    __tablename__ = 'meter_readings'

    meter_readings_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    cold_water = Column(Integer)
    hot_water = Column(Integer)
    datetime = Column(TIMESTAMP)
    is_approved = Column(Boolean)
    is_checked = Column(Boolean, default=0)
    is_initial = Column(Boolean)
    previous_id = Column(Integer, default=None)

    user = relationship("User")


    _session = None  
    def __init__(self, **user_data):
        super().__init__(**user_data)

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session


    @classmethod
    def close_session(cls):
        try:
            if cls._session:
                cls._session.close()
        except Exception as e:
            logger.error(f"Не удалось закрыть сессию: {str(e)}")


    @classmethod
    def get_all(cls):
        try:
            sql = text(
                f"""
                SELECT 
                    *
                FROM
                    resident_bot_db.meter_readings
                ORDER BY datetime DESC;
                """
            )
            object = cls.get_session().execute(sql).fetchall()
            if not object:
                return None
            return object
        except Exception as e:
            logger.error(f"Не удалось получить все показания: {str(e)}")
            return None

    @classmethod
    def get_all_by_checked(cls, is_checked):
        try:
            sql = text(
                f"""SELECT 
                        meter_readings.*,
                        user.*
                    FROM
                        resident_bot_db.meter_readings
                            JOIN
                        resident_bot_db.user ON meter_readings.user_id = user.telegram_id
                    WHERE
                        is_checked = {is_checked}
                    ORDER BY datetime DESC;
                """
            )
            object = cls.get_session().execute(sql, {'is_checked': is_checked}).fetchall()
            if not object:
                return None
            return object
        except Exception as e:
            logger.error(f"Не удалось получить все показания: {str(e)}")
            return None
        
    
    @classmethod
    def get_all_by_checked_and_user_id(cls, is_checked, user_id):
        try:
            sql = text(f"SELECT * FROM resident_bot_db.meter_readings WHERE is_checked = {is_checked} AND user_id = {user_id} ORDER BY datetime DESC;")
            object = cls.get_session().execute(sql, {'is_checked':is_checked, 'user_id':user_id}).fetchall()
            if not object:
                return None
            return object
        except Exception as e:
            logger.error(f"Не удалось получить все показания: {str(e)}")
            return None

        
    @classmethod
    def get_by_id(cls, meter_readings_id):
        try:
            sql = text(f"""
                            SELECT 
                                m1.*,
                                m2.cold_water as prev_cold_water, m2.hot_water as prev_hot_water,
                                user.*,
                                m3.meter_readings_id as has_dependence
                            FROM
                                resident_bot_db.meter_readings AS m1
                                    LEFT JOIN
                                resident_bot_db.user ON m1.user_id = user.telegram_id
                                    LEFT JOIN
                                resident_bot_db.meter_readings AS m2 ON m1.previous_id = m2.meter_readings_id
                                    LEFT JOIN
                                resident_bot_db.meter_readings AS m3 ON m3.previous_id = m1.meter_readings_id
                            WHERE
                                m1.meter_readings_id = {meter_readings_id}
                        """)
            object = cls.get_session().execute(sql, {"meter_readings_id": meter_readings_id}).fetchone()
            if not object:
                return None
            return object
        except Exception as e:
            logger.error(f"Не удалось получить показания по id: {str(e)}")
            return None
        
    @classmethod
    def get_all_by_user_id(cls, user_id):
        try:
            sql = text(
                f"""SELECT 
                        meter_readings.*
                    FROM
                        resident_bot_db.meter_readings
                            JOIN
                        resident_bot_db.user ON meter_readings.user_id = user.telegram_id
                    WHERE
                        user_id = {user_id}
                    ORDER BY datetime DESC;
                """
            )
            session = cls.get_session()
            result = session.execute(sql, {"user_id": user_id}).fetchall()
            return result
        except Exception as e:
            logger.error(f"Не удалось получить показания по user_id = {user_id}: {str(e)}")
            return None
        
    
    @classmethod
    def has_unchecked_by_user_id(cls, user_id):
        try:
            sql = text(
                f"""
                    SELECT 
                        meter_readings.*
                    FROM
                        resident_bot_db.meter_readings
                            JOIN
                        resident_bot_db.user ON meter_readings.user_id = user.telegram_id
                    WHERE
                        user_id = {user_id} and is_checked = 0
                    ORDER BY meter_readings.datetime DESC
                    LIMIT 1;
                """
            )
            session = cls.get_session()
            result = session.execute(sql, {"user_id": user_id}).fetchone()
            if result:
                return result
            return None
        except Exception as e:
            logger.error(f"Не удалось вывести непроверенные показания по user_id = {user_id}: {str(e)}")
            return None
        

    @classmethod
    def get_last_by_user_id(cls, user_id):
        try:
            sql = text(
                f"""
                    SELECT 
                        meter_readings.*
                    FROM
                        resident_bot_db.meter_readings
                            JOIN
                        resident_bot_db.user ON meter_readings.user_id = user.telegram_id
                    WHERE
                        user_id = {user_id} AND is_approved = 1
                    ORDER BY meter_readings.datetime DESC
                    LIMIT 1;
                """
            )
            session = cls.get_session()
            result = session.execute(sql, {"user_id": user_id}).fetchone()
            if not result:
                return None
            return result
        except Exception as e:
            logger.error(f"Не удалось получить последние показания по user_id = {user_id}: {str(e)}")
            return None


    @classmethod
    def delete_by_id(cls, meter_id):
        try:
            meter = cls.get_session().query(cls).filter_by(meter_readings_id=meter_id).one()
            cls.get_session().delete(meter)
            cls.get_session().commit()
            return True
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось удалить показания: {str(e)}")
            return False
    
    @classmethod
    def aprove_by_id(cls, meter_id, user_id):
        try:
            meter = cls.get_session().query(cls).filter_by(meter_readings_id=meter_id).one()
            last_meter = cls.get_last_by_user_id(user_id)
            if meter:
                meter.is_approved = True
                meter.is_checked = True
                if last_meter:
                    meter.previous_id = last_meter.meter_readings_id
                
                cls.get_session().commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось подтвердить показания: {str(e)}")
            return False
        
    @classmethod
    def decline_by_id(cls, meter_id):
        try:
            meter = cls.get_session().query(cls).filter_by(meter_readings_id=meter_id).one()
            if meter:
                meter.is_approved = False
                meter.is_checked = True
                cls.get_session().commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось подтвердить показания: {str(e)}")
            return False
        
    @classmethod
    def check_by_id(cls, meter_id):
        try:
            meter = cls.get_session().query(cls).filter_by(meter_readings_id=meter_id).one()
            if meter:
                meter.is_checked = True
                cls.get_session().commit()
                return True
            else: 
                return False
        except NoResultFound:
            return False
        except Exception as e:
            logger.error(f"Не удалось просмотреть показания: {str(e)}")
            return False
        
        
    @classmethod
    def create_meter(cls, meter_data):
        try:
            new_meter = cls(**meter_data)
            cls.get_session().add(new_meter)
            cls.get_session().commit()
            return new_meter
        except Exception as e:
            logger.error(f"Ошибка при создании показаний: ", str(e))
            return None
   

if __name__ == "__main__":
    engine = create_engine('mysql+mysqlconnector://root:some_pass123@89.111.172.79/resident_bot_db')
    Session = sessionmaker(bind=engine)
    session = Session()

     # # Запрос данных
    # User.set_session(session)
    # users = User.get_all()
    # print(users)

    MeterReading.set_session(session)
    print(MeterReading.get_all_by_user_id(970311146))
    print(MeterReading.get_last_by_user_id(970311146))
    MeterReading.set_session(Session())
    print(MeterReading.get_all())

    print(MeterReading.aprove_by_id(1))
    print(MeterReading.check_by_id(1))
   
    
   
    # ResidentialComplex.set_session(Session())
    # print(ResidentialComplex.get_all())

    # # new_user_data = {
    # #     'telegram_id': 228,
    # #     'first_name': '228',
    # #     'last_name': '228',
    # #     'patronymic': '228',
    # #     'phone_number': '228',
    # #     'email': '228@ex5ample.com',
    # #     'role_id': 1,
    # # }

    # # new_user = User(**new_user_data)
    # # new_user.save()


    # # Вывод результатов
    # print("ТАБЛИЦА ВСЕХ ПОЛЬЗОВАТЕЛЕЙ")
    # for user in users:
    #     print(f"telegram_id: {user.telegram_id}, first_name: {user.first_name}, last_name: {user.last_name}, email: {user.email}")


    # Employer.set_session(session)
    # employers = Employer.get_all()
    # print("ТАБЛИЦА ВСЕХ ГЛАВНЫХ")
    # for employer in employers:
    #     print(f"telegram_id: {employer.telegram_id}, first_name: {employer.first_name}, last_name: {employer.last_name}, email: {employer.email}")


    # current_datetime = datetime.datetime.now()


    # current_date = current_datetime.date()
    # current_time = current_datetime.time()

    # Ticket.set_session(session)
    # TicketType.set_session(session)

    # UtilityBill.set_session(session)
    # all_utility_bills = UtilityBill.get_all()
    # for utility_bill in all_utility_bills:
    #     print(utility_bill.utility_bill_id, utility_bill.user_id, utility_bill.date, utility_bill.due_date, utility_bill.invoice_els_number, utility_bill.amount, utility_bill.description)

    # UserRole.set_session(session)
    

    # print(User.get_user_by_id(2))
    # print(User.exists(266))

    # ticket = TicketType.get_id_by_ticket_type_name("Другое")
    # print(ticket)

    # print(UserRole.get_role_id_by_role_name('Собственник'))

    # EmployerRole.set_session(session)
    # print(EmployerRole.get_role_id_by_role_name('Сотрудник'))



    # print("Все неподтвержденные юзеры")
    # print(User.get_all_unconfirmed_users())
    # print("Все подтвержденные юзеры")
    # print(User.get_all_confirmed_users())

    # print("Все подтвержденные сотрудники")
    # print(Employer.get_all_confirmed_employers())

    # print(Employer.get_by_id(1))
    # print(Employer.exists(2))

    # # emp = Employer.get_by_id(1)
    # # update_data = {
    # #     'first_name':"Новое имя 3"
    # # }
    # # print(emp)
    # # Employer.update_by_id(emp.telegram_id, update_data)
    # # print(emp)

    # print(Employer.get_all_by_role("Сотрудник"))

    
    # print(User.get_user_by_id(2))

    # print(Ticket.get_all_by_user_id_and_status(11583571070, 0))

    # print(TicketType.get_by_id(2).type)

    # Poll.set_session(session)
    # # Poll.create_poll({"poll_tg_id": 1, "message_id": 1, "tittle": 1})
    # print(Poll.get_by_id(1))
    # # Закройте сессию
    # session.close()


