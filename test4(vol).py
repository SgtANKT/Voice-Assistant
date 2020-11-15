import os
import Phase1 as p1
while True:
	audio = p1.get_audio()
	for word in audio:
		if word.isdigit():
			numb = int(word)
	if "increase" in audio:
		os.system(f"setvol +20")
		p1.speak("Okay, increasing volume")
	elif "decrease" in audio:
		os.system(f"setvol -20")
		p1.speak("Okay, Decreasing volume")
	else:
		p1.speak("Say that again please")