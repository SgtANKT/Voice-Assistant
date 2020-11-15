from datetime import *
import pytz
import os

# current_date_and_time = datetime.now()
offset_hours = 5.30
hours_added = timedelta(hours = offset_hours)
a = "04:30:00Z"
b = a.replace("Z","")
c = datetime.strptime(b,'%H:%M:%S')
future_date_and_time = c + hours_added
# future_date_and_time = b + hours_added
a = future_date_and_time.strftime('%I:%M %p')
print(a)
# c= datetime.strptime(a, "%H:%M%S")
# b = c.strftime("%I:%M %p")
# c = datetime.strptime(a, '%H%M').strftime('%I:%M%p').lower()
# print(c)
# print(b)