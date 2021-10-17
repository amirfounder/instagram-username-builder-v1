import requests
from bs4 import BeautifulSoup


THESAURUS_BASE_URL = 'https://www.thesaurus.com/browse'
USERNAME_CHECKER_BASE_URL = 'https://instausername.com/availability?q='


def generate_usernames():
  pass

def check_username_availability(username):
  r = requests.get(f'{USERNAME_CHECKER_BASE_URL}{username}')
  soup = BeautifulSoup(r.text, 'html.parser')
  container = soup.find('div', {'id': 'resmes'})
  return 'is free!' in container.text


def find_synonyms(word):
  r = requests.get(f'{THESAURUS_BASE_URL}/{word}')
  soup = BeautifulSoup(r.text, 'html.parser')
  container = soup.find('div', {'data-testid': 'word-grid-container'})
  links = container.find_all('a')
  return [link.text for link in links]


print(check_username_availability('amirfounder'))