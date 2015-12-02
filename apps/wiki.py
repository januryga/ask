import requests
from bs4 import BeautifulSoup #czytanie htmla

def get_article(article_name):
    """
    Searches wikipedia for given article_name string,
    and returns a string with the title and description
    of the first article found.
    """
    try:
        search_results = api_search(article_name)
        article = search_results[0]
        result = article['title'] + '\n' + article['description']
    except requests.exceptions.ConnectionError:
        result = "ERROR:server is offline."
    except ValueError:
        result = "Sorry, didn't find anything."

    return result
    # for result in results:
    #     if not result['description']:
    #         result['description'] = scrape_article(result['url'])
        
    


def api_search(article_name, lang='pl'):
    """
    Using the MediaWiki API, search wikipedia for given article_name
    and return a list of dicts containing the server's response.
    Each dict contains the keys: 'title', 'description', 'url'.
    """
    url = "http://www.wikipedia.org/w/api.php"
    params = search_params(article_name, lang=lang)

    response = requests.get(url, params)
    if response:
        results_list = response.json()
        results = to_dict(results_list)
        return results
    else:
        raise ValueError("Something's wrong, couldn't download anything.")


# def scrape_article(url):
#     """ Download the wikipedia article with a given name and return its first paragraph."""

#     page = requests.get(url)
#     if page:
#         root = BeautifulSoup(page.text, 'html.parser')
#     else:
#         raise ValueError("Something's wrong, couldn't download anything.")




def search_params(article_name, lang='pl', result_number=2):
    """
    Construct and return a dict containing parameters
    for the Wikipedia MediaWiki API.
    """

    # play around with different parameters or find new ones:
    # https://en.wikipedia.org/wiki/Special:ApiSandbox
    params = {
        'search': article_name,
        'uselang' : lang,
        'limit' : result_number,
        'action': 'opensearch',
        'format': 'json',
        'namespace': 0,
        'redirects': 'return',
        'suggest': ''
    }
    return params


def to_dict(response_array):
    """
    Convert a MediaWiki API JSON response from a messy array to
    a more usable dict format. Expected array format:
    [ search_string, [result_titles], [result_descriptions], [result_urls] ]
    """
    query, titles, descriptions, urls = response_array

    dicted = []
    grouped = zip(titles, descriptions, urls)
    keys = ['title', 'description', 'url']

    for values in grouped:
        element = dict(zip(keys, values))
        dicted.append(element)

    return dicted

