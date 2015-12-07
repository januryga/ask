# -*- coding: cp1250 -*-
""" Reply generating component """

import inspect

import apps.twitch
#import apps.google
import apps.maps
import apps.wiki


def parse_input(input):
	try:
		app, joined_params = input.split(' ', 1)
		dirty_parameters = joined_params.split(',')
		parameters = [param.strip() for param in dirty_parameters]
	except ValueError:
		app, parameters = input, []
	
	return app, parameters



def get_reply(user_message, user_phone=''):
	"""
	Tries to interpret the input from user_message. If the input
	is a valid command, it calls the right app from apps/ with the
	interpreted parameters, and returns its output. (string) If the
	input isn't valid, returns a nice error message. (string)
	"""

	user_message = user_message.lower()
	chosen_app, parameters = parse_input(user_message)
	result = ''

	app_functions = {
		'twitch': apps.twitch.describe_user_status,
		#'google': apps.google.search_results,
		'wiki': apps.wiki.get_article,
		'maps': apps.maps.describe_directions
	}


	try:
		app = app_functions[chosen_app]
		result = app(*parameters)



	# Error Handling


	except KeyError:
		result = "Sorry, there's no app called {app}.".format(app=chosen_app)

	# Confusingly, giving a function a wrong number of arguments raises TypeError.
	except TypeError as error:
		required_arg_num = len(inspect.getargspec(app)[0])
		given_arg_num = len(parameters)

		if required_arg_num > given_arg_num:
			template = (
				"Sorry, {app} requires more parameters. "
				"You gave it {given}, but it needs {required} "
				"to work."
			)
		else:
			template = (
				"Sorry, that's too many parameters for {app} to handle. "
				"You gave it {given}, but it only needs {required} "
				"to work."
			)

		result = template.format(app=chosen_app,
								given=given_arg_num,
								required=required_arg_num)

	# Catch all other errors, just to be sure.
	except:
		result = (
			"Something went really wrong here, and we're not sure what. "
			"Maybe you misspelled something?. The correct input format is:\n"
			"app_name parameter1, parameter2, ..."
		)



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
