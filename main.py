import requests
from bs4 import BeautifulSoup

thesaurus_api_base = 'https://www.thesaurus.com/browse'

def find_synonyms(word):
  r = requests.get(f'{thesaurus_api_base}/{word}')

  soup = BeautifulSoup(r.text, 'html.parser')
  word_grid_container = soup.find('div', {
    'data-testid':
    'word-grid-container'
    })
  links = word_grid_container.find_all('a')
  
  return [link.text for link in links]

synonyms = find_synonyms('hello')
print(synonyms)