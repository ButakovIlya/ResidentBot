import re

def is_valid_email(email: str) -> bool:
    regex = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    return bool(re.fullmatch(regex, email))

def is_valid_name(name: str) -> bool:
    # имя, фамилия, отчество - от 2 до 35 символов (латиница или кириллица)
    # возможны двойное имя и двойная фамилия, которые указываются через дефис/минус/короткое тире/длинное тире
    regex = re.compile(r'^([A-Za-zА-Яа-яЁё]{2,35}([—–−-][A-Za-zА-Яа-яЁё]{2,35})?\s){2}[A-Za-zА-Яа-яЁё]{2,35}$')
    return bool(re.fullmatch(regex, name))
