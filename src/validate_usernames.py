import requests
from bs4 import BeautifulSoup
from src.utils.constants import USERNAME_CHECKER_BASE_URL, USERNAME_MAX_LENGTH

def validate_username(username):
  return \
    is_username_appropriate_length(username) and \
    is_username_available(username)
    

def is_username_appropriate_length(username):
  return len(username) <= USERNAME_MAX_LENGTH

def is_username_available(username):
  r = requests.get(f'{USERNAME_CHECKER_BASE_URL}{username}')
  soup = BeautifulSoup(r.text, 'html.parser')
  try:
    container = soup.find('div', {'id': 'resmes'})
    return 'is free!' in container.text
  except:
    return False