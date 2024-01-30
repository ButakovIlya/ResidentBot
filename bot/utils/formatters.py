from datetime import datetime
import locale

def format_datetime(input_str):
    # Установка русской локали
    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')
    
    # Преобразование строки в объект datetime
    input_datetime = datetime.strptime(str(input_str), '%Y-%m-%d %H:%M:%S')
    
    # Форматирование строки в требуемый вид
    formatted_str = input_datetime.strftime('%d.%m.%Y %H:%M')
    
    return formatted_str

