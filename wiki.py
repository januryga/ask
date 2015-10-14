import requests
from bs4 import BeautifulSoup #czytanie htmla
import re

def get_paragraph(article_name):
    """ Download the wikipedia article of a given name and return its first paragraph."""
    results = api_search(article_name)
    for result in results:
        if not result['description']:
            result['description'] = scrape_paragraph(result['url'])
    return results

def api_search(article_name):
    """
    Search wikipedia for given name and return the server's response in JSON format:
    [ search_string, [result_titles], [result_descriptions], [result_url] ]
    """
    url = "http://www.wikipedia.org/w/api.php"
    params = search_params(article_name, lang='pl')

    response = requests.get(url, params)
    results_list = response.json()

    if results_list:
        results = todict(results_list)
        return results
    else:
        raise ValueError("Something's wrong, couldn't download anything.")


def scrape_paragraph(url):
    """ Download the wikipedia article with a given name and return its first paragraph."""

    page = requests.get(url)
    
    if page:
        root = BeautifulSoup(page.text, 'lxml')
        paragraph = root.p
    
        return paragraph.text
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


def todict( result ):
    """
    Convert a MediaWiki API JSON response from array to a more usable dict format.
    expected array format: [ search_string, [result_titles], [result_descriptions], [result_url] ]
    """

    titles = result[1]
    descriptions = result[2]
    urls = result[3]

    dicted = []
    grouped = zip(titles, descriptions, urls)
    keys = ['title', 'description', 'url']

    for values in grouped:
        element = dict(zip(keys, values))
        dicted.append(element)
    return dicted

