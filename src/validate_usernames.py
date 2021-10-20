import requests
from bs4 import BeautifulSoup
from src.utils.constants import USERNAME_CHECKER_BASE_URL

def check_username_availability(username):
  r = requests.get(f'{USERNAME_CHECKER_BASE_URL}{username}')
  soup = BeautifulSoup(r.text, 'html.parser')
  container = soup.find('div', {'id': 'resmes'})
  return 'is free!' in container.text