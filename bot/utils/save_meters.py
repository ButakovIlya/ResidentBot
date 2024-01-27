from utils.db_requests import create_meter_readings
from datetime import datetime

def save_meter_readings(cold_water, hot_water, user_id):

    meter_data = {
        'cold_water':cold_water,
        'hot_water':hot_water,
        'user_id':user_id, 
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    print(meter_data)
    new_meter = create_meter_readings(meter_data)
    print(new_meter)

    return new_meter