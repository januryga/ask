""" Search Google. Surprising, huh? """

import json
import requests




def pretty_search(query):
    """ pretty_search(string) -> string

    Searches google and returns a printable string of results
    or a friendly error message. Handles: 
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
    """printable_string(list) -> string

    Returns a string, created by combining the given search_results.
    Results are separated by newlines.
    The dicts must contain "titleNoFormatting" and "content".
    Raises ValueError if the argument list is empty."""

    if search_results:
        str_list=[]
        for res in search_results:
            title = res['titleNoFormatting']
            content = res['content']
            str_list.append(title + content)
        result = '\n'.join(str_list)
    else:
        raise ValueError("The search_results list you passed is empty.")

    return result



def search_results(query):
    """search_results(string) -> list

    Returns a list containing Google Search results for
    given query. If no results are found, returns an empty
    list."""

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0'
    resp = requests.get( url, params={'q': query} )
    json_bytes = resp.content
    json_text = json_bytes.decode('utf-8')
    json_dict = json.loads(json_text)

    search_results = json_dict['responseData']['results']
    
    return search_results
