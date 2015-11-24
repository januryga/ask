""" Reply generating component """

def get_reply(user_message):
	"""
	Tries to interpret the input from user_message. If the input
	is a valid command, it calls the right app from apps/ with the
	interpreted parameters, and returns its output. (string) If the
	input isn't valid, returns a nice error message. (string)
	"""

	import apps.twitch
	import apps.google_maps
	import apps.google
	import apps.wikipedia
	input=user_message
	input=input.lower()
	
	input_list=[None,None,None,None,None]
	
	i=0
	for word in input.split(','):
	    input_list[i]=word
	    i=i+1
	    if i>4:
	        break
	
	program=input_list[0]
	parameter1=input_list[1]
	parameter2=input_list[2]
	parameter3=input_list[3]
	parameter4=input_list[4]
	
	"""
	return ("Requested program: " + program)
	return ("Parameters: ")
	
	for word in input_list[1:]:
	    if word:
	        return (word + " ")
	"""
	if not parameter1 and " " in program:
	    return ("ERROR: No parameters found for \"" + program.split(' ')[0] +"\".\nPlease separate expressions with \",\".")
	elif not program:
	    return ("ERROR: Empty request")
	elif program=="maps" or program=="google maps":
	    if not parameter1 or not parameter2 or not parameter3:
	        return ("ERROR: To few parameters")
	    elif parameter4:
	        return ("ERROR: To many parameters")
	    else:
	        return (Google_maps.find_path_city_a_b(parameter1,parameter2,parameter3))
	elif program=="twitch":
	    if not parameter1:
	        return ("ERROR: To few parameters")
	    elif parameter2 or parameter3:
	        return ("ERROR: To many parameters")
	    else:
	        return (Twitch.get_online_status(parameter1))
	elif program=="wiki" or program=="wikipedia":
	    if not parameter1:
	        return ("ERROR: To few parameters")
	    elif parameter2:
	        return ("ERROR: To many parameters")
	    else:
	        return (Wikipedia.TU WPISZ NAZW  FUKNCJI, KT”RA ZWRACA ODPOWIEDè(parameter1))
	elif program=="google":
	    if not parameter1:
	        return ("ERROR: To few parameters")
	    elif parameter2:
	        return ("ERROR: To many parameters")
	    else:
	        return (Google.get_google_search(parameter1))
	else:
	    return ("ERROR: \"" + program + "\" - No such service provided")
	return reply_message

# About the error message: It should make clear what the error actually is.
# The error cases I could think of:
#
# ---- USER ERRORS ----
# 1) Invalid app
# 2) Valid app, invalid parameters:
#   a) Valid app, can't understand parameters
#   b) Valid app, not enough parameters
#   c) Valid app, too many parameters
# ---- OTHER ERRORS ----
# 3) Valid app, valid parameters, but the app found no results.
#      Example: no results from google search
# 4) The app is currently unavailable (because google maps is down or sth)
