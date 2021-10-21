import requests
from bs4 import BeautifulSoup
from os.path import exists, isdir
from os import mkdir

from src.utils.constants import THESAURUS_BASE_URL, ADJECTIVES
from src.utils.utils import \
  create_file, \
    get_from_file, \
      write_to_file, \
        run_concurrently_using_threads


SYNONYMS_FILE, UTILIZED_FILE, UNIQUE_SYNONYMS_FILE = None, None, None

def build_adjectives():
  for adjective in ADJECTIVES:
    build_keywords_using_synonyms(adjective)


def get_adjectives():
  all_adjectives = []

  for adjective in ADJECTIVES:
    data = get_from_file(f'data/synonyms/{adjective}/unique.txt')
    data_as_list = data.split('\n')
    all_adjectives.extend(data_as_list)
  
  return list(set(all_adjectives))


def build_keywords_using_synonyms(seed: str):
  seed.replace(' ', '-')
  global SYNONYMS_FILE, UTILIZED_FILE, UNIQUE_SYNONYMS_FILE

  if not isdir('data'):
    mkdir('data')

  if not isdir(f'data/synonyms'):
    mkdir(f'data/synonyms')
  
  if not isdir(f'data/synonyms/{seed}'):
    mkdir(f'data/synonyms/{seed}')


  synonyms_file = f'data/synonyms/{seed}/raw.txt'
  utilized_file = f'data/synonyms/{seed}/utilized.txt'
  unique_synonyms_file = f'data/synonyms/{seed}/unique.txt'

  if exists(synonyms_file) \
    or exists(utilized_file) \
      or exists(unique_synonyms_file):
    print(f'Already have files for seed word: {seed}')
    return

  create_file(synonyms_file)
  create_file(utilized_file)
  create_file(unique_synonyms_file)

  SYNONYMS_FILE = synonyms_file
  UTILIZED_FILE = utilized_file
  UNIQUE_SYNONYMS_FILE = unique_synonyms_file

  depth = 2
  i = 0
  add_to_synonyms(seed)

  while i < depth:
    print(f'current depth level: {i}')

    fns_args = []
    synonyms = get_from_synonyms()
    for synonym in synonyms:
      fns_args.append((
        find_and_write_synonyms_to_file,
        (synonym,)
      ))

    run_concurrently_using_threads(fns_args)
    i += 1
  
  build_unique_synonyms_file()


def find_and_write_synonyms_to_file(word):
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


def build_unique_synonyms_file():
  synonyms = get_from_synonyms()
  unique_synonyms = list(set(synonyms))
  with open(UNIQUE_SYNONYMS_FILE, 'a') as f:
    for unique_synonym in unique_synonyms:
      f.write(f'{unique_synonym}\n')


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
