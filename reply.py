# -*- coding: cp1250 -*-
""" Reply generating component """

import re

#import apps.google as google
import apps.google_maps as google_maps
import apps.wiki as wiki
import apps.twitch as twitch




def grind_input(input):
	app = input.split(' ')[0]
	parameters = input.partition(' ')[2]
	parameters = parameters.split(',')
	for index,parameter in enumerate(parameters):
		if parameters[index]=='':
			parameters.pop(index)
	return app,parameters

def get_reply(user_message):
	"""
	Tries to interpret the input from user_message. If the input
	is a valid command, it calls the right app from apps/ with the
	interpreted parameters, and returns its output. (string) If the
	input isn't valid, returns a nice error message. (string)
	"""

	user_message = user_message.lower()
	chosen_app, parameters = grind_input(user_message)
	result = ''

	apps = {
		'twitch': twitch.get_online_status,
		#'google':google.search,
		'wiki': wiki.get_article,
		'maps': google_maps.find_path_city_a_b
	}

	try:
		app = apps[chosen_app]
		result = app(*parameters)
		
	except KeyError:
		result = "Sorry, there's no app with this name."
	except TypeError as error:
		if re.findall(r'\d+',error.args[0])[0]>re.findall(r'\d+',error.args[0])[1]:
			result = ("Sorry, this app requires more parameters.")
		else:
			result = ("Sorry, that's too many parameters for this app.")
	except twitch.WrongUsernameError:
		result = ("orry, couldn't find a user with that name.")
	except:
		result = """Something went really wrong here, and we're not sure what.
					Maybe you misspelled something?. The correct input format is:
					app_name parameter1, parameter2, ..."""

	return result
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
