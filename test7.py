import datetime
import pytz
utc = pytz.utc
# utc.zone
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc_dt = utc.localize(datetime.datetime.now())

utc_dt.strftime(fmt)
print(utc_dt)
# '2006-03-26 21:34:59 UTC+0000'
in_tz = pytz.timezone('Asia/Kolkata')
# in_dt = utc_dt.astimezone(in_tz)
# in_dt.strftime(fmt)
# print(in_dt)
# # '2006-03-27 08:34:59 AEDT+1100'
# utc_dt2 = in_dt.astimezone(utc)
# utc_dt2.strftime(fmt)
# print(utc_dt2)
# # '2006-03-26 21:34:59 UTC+0000'
# # utc_dt == utc_dt2
utc_dt = datetime.datetime(1915, 8, 4, 22, 36, tzinfo=pytz.utc)
a = utc_dt.astimezone(in_tz).strftime(fmt)
print(utc_dt)
print(a)
# '1915-08-04 23:36:00 CET+0100'