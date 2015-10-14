import requests
from bs4 import BeautifulSoup #czytanie htmla

def get_paragraph(article_name):
    """ Download the wikipedia article of a given name and return its first paragraph.""" 
    
    url = "http://en.wikipedia.org/wiki/" + article_name.strip()
    page = requests.get(url)
    
    if page:
        root = BeautifulSoup(page.text, 'lxml')
        paragraph = root.p
    
        return paragraph.text
    else:
        return "Something's wrong, couldn't download anything."

