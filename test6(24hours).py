import Phase1 as p1


# p1.speak("What would you like to keep the summary?")
# summary = p1.get_audio()
# print(summary)
# p1.speak("What would be the location of this event?")
# location = p1.get_audio()
# print(location)
# p1.speak("Do you want to add the description?")
# confirmation = p1.get_audio()
# print(confirmation)
# if "yes" in confirmation:
# 	description = p1.get_audio()
# elif "no" in confirmation:
# 	p1.speak("Okay got it. No description added")
# else:
# 	p1.speak("Sorry I did not catch that")
# p1.speak("What should be the date?")
# date_text = p1.get_audio()
# date = p1.get_date(date_text)
# print(date)

# p1.speak("What shall be the time?")
# # time_text = p1.get_audio()
# # print(time_text)
#
# # 	TIME_VALUSE=["am, pm"]
# # for value in TIME_VALUSE:
# # 	if value in time_text:
# # 		_ = value
# # 		if _:
# # 			print(f"YES I AM {value}")
#
#
#
# text = p1.get_audio()
# print(text[-4:])


import datetime
# m2 = '1:35 AM'

a = p1.get_audio()
if ".m." in a:
	s = str(a.replace(".", "").upper())
	if ":" in s:
		start_time_temp = datetime.datetime.strptime(s, '%I:%M %p')
		start_time = start_time_temp.strftime('%H:%M:%S')
		print(start_time)
		print("okay")
	else:
		output_line = s[:2] + ':00'.replace(" ", "") + " PM"
		start_time_temp = datetime.datetime.strptime(output_line, '%I:%M %p')
		start_time = start_time_temp.strftime('%H:%M:%S')
		print(start_time)
# import datetime
# now_time = datetime.datetime.now()
# print(now_time)
# hours = 5.30
# hours_added = datetime.timedelta(hours = hours)
# print(hours)
# add = now_time + hours_added
# print(add)