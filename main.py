import requests
from bs4 import BeautifulSoup
from time import time
from threading import Thread
from os.path import exists


THESAURUS_BASE_URL = 'https://www.thesaurus.com/browse'
USERNAME_CHECKER_BASE_URL = 'https://instausername.com/availability?q='
SYNONYMS_FILE = 'synonyms.txt'
UTILIZED_FILE = 'utilized.txt'
USERNAME_MAX_LENGTH = 30


def run_concurrently_using_threads(fns_args: list[tuple[object, tuple]]):
  threads = []
  for fn, args in fns_args:
    threads.append(Thread(target=fn, args=args))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()


def generate_usernames():
  pass

def check_username_availability(username):
  r = requests.get(f'{USERNAME_CHECKER_BASE_URL}{username}')
  soup = BeautifulSoup(r.text, 'html.parser')
  container = soup.find('div', {'id': 'resmes'})
  return 'is free!' in container.text

def generate_potential_usernames():
  pass


def generate_keywords_using_synonyms(seed):
  global SYNONYMS_FILE, UTILIZED_FILE

  synonyms_file = f'data/{seed}_synonyms.txt'
  utilized_file = f'data/{seed}_utilized.txt'

  if exists(synonyms_file) or exists(utilized_file):
    print(f'Already have files for seed word: {seed}')
    return

  create_file(synonyms_file)
  create_file(utilized_file)

  SYNONYMS_FILE = synonyms_file
  UTILIZED_FILE = utilized_file

  depth = 2
  i = 0
  add_to_synonyms(seed)

  while i < depth:
    print(f'current depth level: {i}')

    fns_args = []
    synonyms = get_from_synonyms()
    for synonym in synonyms:
      fns_args.append((find_and_add_synonyms_to_global, (synonym,)))

    run_concurrently_using_threads(fns_args)
    i += 1


def find_and_add_synonyms_to_global(word):
  persisted_synonyms = get_from_synonyms()
  local_synonyms = find_synonyms(word)
  for local_synonym in local_synonyms:
    if local_synonym not in persisted_synonyms:
      add_to_synonyms(local_synonym)

def find_synonyms(word):
  global requests_made
  utilized = get_from_utilized()
  if word not in utilized:
    r = requests.get(f'{THESAURUS_BASE_URL}/{word}')
    add_to_utilized(word)
    print(f'request made!')
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
      container = soup.find('div', {'id': 'meanings'})
      try:
        links = container.find_all('a')
        return [link.text for link in links]
      except:
        return []
    except:
      return []
  else:
    print(f'already utilized: {word}')
    return []


def get_from_synonyms():
  data = get_from_file(SYNONYMS_FILE)
  synonyms = data.split('\n')
  return [synonym for synonym in synonyms if synonym != '']

def add_to_synonyms(synonym):
  write_to_file(SYNONYMS_FILE, synonym)

def get_from_utilized():
  data = get_from_file(UTILIZED_FILE)
  return data.split('\n')

def add_to_utilized(utilized_word):
  write_to_file(UTILIZED_FILE, utilized_word)

def get_from_file(file):
  f = open(file, 'r')
  data = f.read()
  f.close()
  return data

def write_to_file(file, content):
  f = open(file, 'a')
  f.write(f'{content}\n')
  f.close()

def create_file(file):
  f = open(file, 'a')
  f.close()
  return file

def generate_unique_file():
  syns = get_from_synonyms()
  unique_syns = list(set(syns))
  with open('unique_syns.txt', 'a') as f:
    for unique_syn in unique_syns:
      f.write(unique_syn)
      f.write('\n')

if __name__ == '__main__':
  generate_keywords_using_synonyms('money')
