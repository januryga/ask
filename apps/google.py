""" Search Google. Surprising, huh? """

import json
import requests
import re



def pretty_search(query):
	"""Searches google and returns the results (or errors) as a friendly string.

	The actual formatting is done in printable_string, this function is mostly
	for error messages and handling.
	Handles: 
	- ConnectionError (requests module)
	- ValueError (printable_string)"""

	try:
		results = search_results(query)
		answer = printable_string(results)

	except requests.exceptions.ConnectionError:
		answer = "Sorry, couldn't connect to Google."
	except ValueError:
		answer = "Sorry, couldn't find anything for \"{search}\"".format(search=name)
	return answer



def printable_string(search_results):
	"""Returns a string, created by combining the given search_results.

	Results are separated by newlines.
	The dicts must contain "titleNoFormatting" and "content".
	Raises ValueError if the argument list is empty."""

	if search_results:
		str_list=[]
		for res in search_results:
			title = res['titleNoFormatting']
			content = res['content']
			str_list.append(title + '\n' + content)
		dirty_result = '\n\n'.join(str_list)
		result = html_removed(dirty_result)

		return result

	else:
		raise ValueError("The search_results list you passed is empty.")




def search_results(query, res_num=2):
	"""Returns a list of Google Search results.
	
	A single search result is a dict with items such as 'titleNoFormatting'
	and 'content'. More information is available in Google's API docs - all
	this function does is parse the API's JSON response.

	To remove the result limit, set res_num to -1. That will skip this function's
	internal trimming and give you everything Google sent.

	The API's url is:
	http://ajax.googleapis.com/ajax/services/search/web?v=1.0"""

	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0'
	resp = requests.get( url, params={'q': query} )
	json_bytes = resp.content
	json_text = json_bytes.decode('utf-8')
	json_dict = json.loads(json_text)

	search_results = json_dict['responseData']['results']
	
	return search_results[:res_num]



def html_removed(string):
	"""Returns the string without html tags."""
	clean_string = re.sub('<.+?>', '', string)
	return clean_string
