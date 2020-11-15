import parsedatetime as pdt
import speech_recognition as sr
import pyttsx3

test_text = [
	'day after tomorrow',
	'the day after tomorrow',
	'a day after tomorrow',
	'an day after tomorrow',
	'one day after tomorrow',
	'two day after tomorrow',
]


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


def dates(text):
	cal = pdt.Calendar()
	if text in test_text:
		result = cal.nlp(text)[0]
		print("Got: %s  from:'%s'  original:'%s'" % (
			result[0].date(), result[-1], text))


text = get_audio()
dates(text)