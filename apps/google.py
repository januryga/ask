import json
import requests

def get_google_search(name):
    try:
        answer = google_that(name)
    except requests.exceptions.ConnectionError:
        answer = "Sorry, couldn't connect to Google."
    except ValueError:
        answer = "Sorry, couldn't find anything for \"{search}\"".format(search=name)
    return answer

def google_that(thing):
    search_results = get_results(thing)
    str_list=[]
    for res in search_results:
        title = res['titleNoFormatting']
        content = res['content']
        str_list.append(title+content)
    result = '\n'.join(str_list)
    return result

def get_results(phrase):
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0'
    re = requests.get( url, params={'q':phrase} )
    json_data = json.loads(re.content.decode('utf-8'))
    search_result = json_data['responseData']['results']
    if search_result:
        result=search_result
    else:
        raise ValueError
    return result  
