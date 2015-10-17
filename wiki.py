import requests
from bs4 import BeautifulSoup #czytanie htmla

def get_article(article_name):
    """ Download the first paragraph of the wikipedia article with a given name. """

    results = api_search(article_name)
    for result in results:
        if not result['description']:
            result['description'] = scrape_article(result['url'])
    return results


def api_search(article_name, lang='pl'):
    """
    Using the MediaWiki API, search wikipedia for given name and return the server's response in JSON format:
    [ search_string, [result_titles], [result_descriptions], [result_url] ]
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


def scrape_article(url):
    """ Download the wikipedia article with a given name and return its first paragraph."""

    page = requests.get(url)
    if page:
        root = BeautifulSoup(page.text, 'lxml')
    else:
        raise ValueError("Something's wrong, couldn't download anything.")




def search_params(article_name, lang='pl', result_number=2):
    """ Construct and return a dict containing parameters for the Wikipedia MediaWiki API """

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
    Convert a MediaWiki API JSON response from array to a more usable dict format.
    expected array format: [ search_string, [result_titles], [result_descriptions], [result_urls] ]
    """

    titles = response_array[1]
    descriptions = response_array[2]
    urls = response_array[3]

    dicted = []
    grouped = zip(titles, descriptions, urls)
    keys = ['title', 'description', 'url']

    for values in grouped:
        element = dict(zip(keys, values))
        dicted.append(element)

    return dicted

