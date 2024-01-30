from utils.db_requests import create_meter_readings, get_last_meters_by_user
from datetime import datetime

def save_meter_readings(cold_water, hot_water, user_id):
    meter_data = {
        'cold_water':cold_water,
        'hot_water':hot_water,
        'user_id':user_id, 
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        # 'previous_id':last_meters.meter_readings_id
    }

    last_meters = get_last_meters_by_user(user_id)
    
    if last_meters:
        meter_data['previous_id'] = last_meters.meter_readings_id
        meter_data['is_initial'] = False
    else: 
        meter_data['previous_id'] = None
        meter_data['is_initial'] = True


    new_meter = create_meter_readings(meter_data)

    return new_meter