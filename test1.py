import speech_recognition as sr
import pyttsx3
import pytz
import datetime
import Phase1 as p1

WAYS = ["today", "tomorrow"]


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""
		
		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			print("Exception: " + str(e))
	
	return said


def speak(audio):
	engine = pyttsx3.init()
	# anything we pass inside engine.say(),
	# will be spoken by our voice assistant
	engine.say(audio)
	engine.runAndWait()


def get_events(day, service):
	offset_hours = 5.42
	hours_added = datetime.timedelta(hours=offset_hours)
	date = datetime.datetime.combine(day, datetime.datetime.min.time())
	end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
	utc = pytz.UTC
	date = date.astimezone(utc)
	end_date = end_date.astimezone(utc)
	
	events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
	                                      singleEvents=True,
	                                      orderBy='startTime').execute()
	print(events_result)
	events = events_result.get('items', [])
	
	# NEW STUFF STARTS HERE
	if not events:
		speak('No upcoming events found.')
	else:
		speak(f"You have {len(events)} events on this day.")
		
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			# print(start, event['summary'])
			print(event["summary"])
			_start_time = str(start.split("T")[1].split("-")[0])  # get the hour the event starts
			# Getting ist timing
			time_split = _start_time.replace("Z", "")
			str_to_dt = datetime.datetime.strptime(time_split, '%H:%M:%S')
			future_date_and_time = str_to_dt + hours_added
			fin_time = future_date_and_time.strftime('%H:%M:%S') # 24 hours clock
			fin_time_12_hrs = future_date_and_time.strftime('%I:%M %p') # 12 hours clock
			if int(fin_time.split(":")[0]) < 12:  # if the event is in the morning
				start_time_ist = fin_time_12_hrs
				start_time_utc = _start_time + "am"
			else:
				start_time = str(int(_start_time.split(":")[0]) - 12)+ fin_time.split(":")[1]
				# print(start_time)
				start_time_ist = fin_time_12_hrs
				start_time_utc = start_time + "pm"
			
			speak(event["summary"] + " at " + start_time_ist + "Indian Standard time, and at" + start_time_utc + "UTC")


SERVICE = p1.authenticate_google()
day = datetime.date(2020,11,21)
get_events(day, SERVICE)
