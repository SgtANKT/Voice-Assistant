import Phase1 as p1
import datetime
import pytz

service = p1.authenticate_google()

p1.speak("What would you like to keep the summary?")
summary = p1.get_audio()
p1.speak("What would be the location of this event?")
location = p1.get_audio()
p1.speak("Do you want to add the description?")
confirmation = p1.get_audio()
# confirmation = "No"
# while len(confirmation) > 0:
if "yes" in confirmation:
	description = p1.get_audio()
	p1.speak("Description added")
elif 'No' in confirmation:
	p1.speak("Okay")
# description = description
p1.speak("When would you like to keep it?")
date_text = p1.get_audio()
# date_text = "17th November"
date = p1.get_date(date_text)
print(date)
p1.speak("What would be the start time?")
start_audio = p1.get_audio()
# start_audio = "12:30 a.m."
if ".m." in start_audio:
	s = str(start_audio.replace(".","").upper())
	m2 = datetime.datetime.strptime(s, '%I:%M %p')
	converted_time = m2.strftime('%H:%M:%S')
	print(converted_time)
# print(converted_time)
strt_combined_date = str(date)+"T"+converted_time+"Z"
# date_time_obj = datetime.datetime.strptime(combined_date, f'%Y-%m-%d{"T"}%H:%M:%S{"+5:30"}')
# print(combined_date)
tz = "UTC"
p1.speak("What would be the end time?")
end_audio = p1.get_audio()
if ".m." in end_audio:
	s = str(end_audio.replace(".","").upper())
	m2 = datetime.datetime.strptime(s, '%I:%M %p')
	converted_time = m2.strftime('%H:%M:%S')
# print(converted_time)
end_combined_date = str(date)+"T"+converted_time+"Z"
event = {
	'summary': summary,
	'location': location,
	# 'description': description,
	'start': {
		'dateTime': strt_combined_date,
		'timeZone': tz,
	},
	'end': {
		'dateTime': end_combined_date,
		'timeZone': tz,
	},
	'recurrence': [
		'RRULE:FREQ=DAILY;COUNT=2'
	],
	# 'attendees': [
	# 	{'email': 'lpage@example.com'},
	# 	{'email': 'sbrin@example.com'},
	# ],
	# 'reminders': {
	# 	'useDefault': False,
	# 	'overrides': [
	# 		{'method': 'email', 'minutes': 24 * 60},
	# 		{'method': 'popup', 'minutes': 10},
	# 	],
	# },
}

print(event.items())
#
event = service.events().insert(calendarId='primary', body=event).execute()
# print('Event created: %s' % (event.get('htmlLink')))