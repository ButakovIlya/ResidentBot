import datetime

def get_current_date_and_time():
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    return current_date, current_time