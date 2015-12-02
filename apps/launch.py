# -*- coding: cp1250 -*-
""" Reply generating component """

def grind_input(input):
    app=input.split(' ')[0]
    parameters=input.partition(' ')[2]
    parameters=parameters.split(',')
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

    import google as google
    import google_maps as google_maps
    import wiki as wikipedia
    import twitch as twitch
    import re

    user_message=user_message.lower()
    app,parameters=grind_input(user_message)

    apps={
    'twitch':twitch.get_online_status,
    'google':google.get_google_search,
    'wiki':wikipedia.get_article,
    'maps':google_maps.find_path_city_a_b
    };

    try:
        return (apps[app](*parameters))
    except TypeError as error:
        if re.findall(r'\d+',error.args[0])[0]>re.findall(r'\d+',error.args[0])[1]:
            return ("ERROR: To few arguments given.")
        else:
            return ("ERROR: To many arguments given.")
    except Twitch.WrongUsernameError:
        return ("ERROR: Wrong Username")
    except:
        return "Congrats, You found an unhandable error! Now You can try inserting a correct output (format: \"[service] [parameter1],[parameter2]...\")"

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
