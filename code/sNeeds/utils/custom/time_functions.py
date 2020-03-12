import pytz
from khayyam import JalaliDatetime


def utc_to_jalali_string(utc_dt):
    utc_time = utc_dt.astimezone(pytz.timezone('Asia/Tehran'))
    return JalaliDatetime(utc_time).strftime('%C')
