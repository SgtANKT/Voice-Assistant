from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", 'october', "november",
          "december"]
DAY_EXTENTIONS = ["rd", "st", "th", "nd"]


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


def authenticate_google():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	
	service = build('calendar', 'v3', credentials=creds)
	
	return service


def get_events(day, service):
	offset_hours = 5.45
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
			start_time = str(start.split("T")[1].split("-")[0])  # get the hour the event starts
			# Getting ist timing
			time_split = start_time.replace("Z", "")
			str_to_dt = datetime.datetime.strptime(time_split, '%H:%M:%S')
			future_date_and_time = str_to_dt + hours_added
			fin_time = future_date_and_time.strftime('%H:%M:%S')
			if int(fin_time.split(":")[0]) < 12:  # if the event is in the morning
				start_time_ist = fin_time + "am"
				start_time_utc = start_time + "am"
			else:
				start_time = str(int(fin_time.split(":")[0]) - 12) + fin_time.split(":")[1]
				# print(start_time)
				start_time_ist = fin_time + "pm"
				start_time_utc = start_time + "pm"
			
			speak(event["summary"] + " at " + start_time_ist + "IST" + "and at" + start_time_utc + "UTC")


def get_date(text):
	text = text.lower()
	today = datetime.date.today()
	
	if text.count("today") > 0:
		return today
	
	day = -1
	day_of_week = -1
	month = -1
	year = today.year
	
	for word in text.split():
		if word in MONTHS:
			month = MONTHS.index(word) + 1
		elif word in DAYS:
			day_of_week = DAYS.index(word)
		elif word.isdigit():
			day = int(word)
		else:
			for ext in DAY_EXTENTIONS:
				found = word.find(ext)
				if found > 0:
					try:
						day = int(word[:found])
					except:
						pass
	

	if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
		year = year + 1
	
	
	if month == -1 and day != -1:  # if we didn't find a month, but we have a day
		if day < today.day:
			month = today.month + 1
		else:
			month = today.month
	
	# if we only found a dta of the week
	if month == -1 and day == -1 and day_of_week != -1:
		current_day_of_week = today.weekday()
		dif = day_of_week - current_day_of_week
		
		if dif < 0:
			dif += 7
			if text.count("next") >= 1:
				dif += 7
		
		return today + datetime.timedelta(dif)
	
	if day != -1:  # FIXED FROM VIDEO
		return datetime.date(month=month, day=day, year=year)


def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":", "-") + "-note.txt"
	with open(file_name, "w") as f:
		f.write(text)
	
	subprocess.Popen(["notepad.exe", file_name])


def add_events(service):
	speak("What would you like to keep the summary?")
	summary = get_audio()
	speak("What would be the location of this event?")
	location = get_audio()
	speak("Do you want to add the description?")
	confirmation = get_audio()
	if "yes" in confirmation:
		speak("What would you like to add?")
		description = get_audio()
		speak("Description added")
	elif 'No' in confirmation:
		speak("Okay")
	speak("When would you like to keep it?")
	date_text = get_audio()
	date = get_date(date_text)
	speak("What would you like to keep the start time between 12 AM and 5:30 PM?")
	start_audio = get_audio()
	if ".m." in start_audio:
		s = str(start_audio.replace(".", "").upper())
		if ":" in s:
			start_time_temp = datetime.datetime.strptime(s, '%I:%M %p')
			start_time = start_time_temp.strftime('%H:%M:%S')
		else:
			output_line = s[:2] + ':00'.replace(" ", "") + " PM"
			start_time_temp = datetime.datetime.strptime(output_line, '%I:%M %p')
			start_time = start_time_temp.strftime('%H:%M:%S')

	strt_combined_date = str(date) + "T" + str(start_time) + "Z"
	tz = "UTC"
	speak("What would you like to keep the end time between 12 AM and 6:30 PM?")
	end_audio = get_audio()
	if ".m." in end_audio:
		s = str(end_audio.replace(".", "").upper())
		if ":" in s:
			end_time_temp = datetime.datetime.strptime(s, '%I:%M %p')
			end_time = end_time_temp.strftime('%H:%M:%S')
		else:
			output_line = s[:2] + ':00'.replace(" ", "") + " PM"
			end_time_temp = datetime.datetime.strptime(output_line, '%I:%M %p')
			end_time = end_time_temp.strftime('%H:%M:%S')
	end_combined_date = str(date) + "T" + str(end_time) + "Z"
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
	event = service.events().insert(calendarId='primary', body=event).execute()
	print('Event created: %s' % (event.get('htmlLink')))
	return speak("I have added your event")


def increase_vol():
	speak("Volume will be increased or decreased by 20%. What would you like to do, increase or decrease?")
	audio = get_audio()
	if "increase" in audio:
		os.system("setvol +20")
		speak("Okay, increasing volume")
	elif "decrease" in audio:
		os.system("setvol -20")
		speak("Okay, Decreasing volume")
	else:
		speak("Say that again please")


if __name__ == "__main__":
	SERVICE = authenticate_google()
	WAKE = "man"
	while True:
		print("I am Listening")
		text = get_audio()
		
		if text.count(WAKE) > 0:
			speak("I am ready")
			text = get_audio()
			# print("From txt", text)
			# PHRASES = ["What do I have", "What is my schedule", "Do I have any events on"]
			# for phrase in PHRASES:
			#     if phrase in text:
			date = get_date(text)
			# print("From date", date)
			if date:
				get_events(date, SERVICE)
			# else:
			# 	speak("I don't understand")
			INC_STRS = ["raise volume", 'lower volume', 'increase volume', 'decrease volume']
			for stri in INC_STRS:
				if stri in text:
					increase_vol()
			
			
			ADD_STRS = ["add an event", "set an event", "make an event"]
			for string in ADD_STRS:
				if string in text:
					add_events(SERVICE)
			NOTE_STRS = ["make a note", "write this down", "remember this"]
			for phrase in NOTE_STRS:
				if phrase in text:
					speak("What would you like me to write down?")
					note_text = get_audio()
					note(note_text)
					speak("I've made a note of that.")
		if "exit" in text:
			speak("would you like to shutdown or restart your computer or stop the program?")
			text = get_audio()
			if "restart" in text:
				speak("Restarting Computer")
				os.system("shutdown /r /t 15")
				break
			if "shutdown" in text:
				# Shutting down
				speak("Shutting the computer")
				os.system("shutdown /s /t 15")
				break
			if "no" in text:
				speak("Okay Not Restarting or Shutting down for now")
				continue
			if "stop" in text:
				speak("Okay, just rerun me when you want help")
				break
			speak("Say that again sir")