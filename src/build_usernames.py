from os import mkdir
from src.build_keywords import build_keywords_using_synonyms, get_adjectives
from src.utils.utils import create_file, get_from_file, write_to_file
from src.utils.constants import INVALID_USERNAME_CHARACTERS
from os.path import exists



MAX_TOKENS_IN_USERNAME = 3

DELIMETER_STRATEGY_MAP = {
  'default': '',
  'underscore': '_',
  'double_underscore': '__',
  'dash': '-',
  'double_dash': '--',
  'dot': '.'
}

DELIMETER_STRATEGIES = [
  'default',
  'underscore',
  'dot'
]

def double_last_char(token):
  return f'{token}{token[-1:]}'

def triple_last_char(token):
  return f'{token}{token[-1:]}{token[-1:]}'

def double_first_char(token):
  return f'{token[:1]}{token}'

def triple_first_char(token):
  return f'{token[:1]}{token[:1]}{token}'

LETTERING_STRATEGY_MAP = {
  'default': lambda x: x,
  'first_token_last_letter_twice': double_last_char,
  'first_token_last_letter_thrice': triple_last_char,
  'first_token_first_letter_twice': double_first_char,
  'first_token_first_letter_thrice': triple_first_char,
  'last_token_last_letter_twice': double_last_char,
  'last_token_last_letter_thrice': triple_last_char,
  'last_token_first_letter_twice': double_first_char,
  'last_token_first_letter_thrice': triple_first_char,
}

LETTERING_STRATEGIES = ['default']


def build_potenial_usernames(topic):

  if not exists('data'):
    mkdir('data')

  if not exists('data/usernames'):
    mkdir('data/usernames')

  potential_usernames_path = f'data/usernames/{topic}.txt'

  if exists(potential_usernames_path):
    print(f'Generated usernames already exist for topic: {topic}')
  else:
    create_file(potential_usernames_path)


  potential_usernames = []

  synonyms = get_unique_synonyms(topic)
  adjectives = get_adjectives()

  # build usernames with 1 synonym
  potential_usernames.extend(synonyms)

  # build usernames with 2 synonyms + all combos of delimeters, synonyms
  local_potentials1 = build_potential_usernames_combos(
    synonyms,
    synonyms,
    DELIMETER_STRATEGIES,
    LETTERING_STRATEGIES
  )
  print('Built all potential usernames with [syn][del][syn] combo')
  local_potentials2 = build_potential_usernames_combos(
    synonyms,
    adjectives,
    DELIMETER_STRATEGIES,
    LETTERING_STRATEGIES
  )
  print('Built all potential usernames with [syn][del][adj] combo')
  local_potentials3 = build_potential_usernames_combos(
    adjectives,
    synonyms,
    DELIMETER_STRATEGIES,
    LETTERING_STRATEGIES
  )
  print('Built all potential usernames with [adj][del][syn] combo')

  potential_usernames.extend(local_potentials1)
  potential_usernames.extend(local_potentials2)
  potential_usernames.extend(local_potentials3)
  
  write_to_file(
    potential_usernames_path,
    '\n'.join(potential_usernames)
  )

  return potential_usernames

  # TODO
  # build usernames with 3 synonyms + all combos of delimeters, synonyms
    # syn [del] syn [del] syn
    # syn [del] syn [del] adj
    # syn [del] adj [del] syn
    # adj [del] syn [del] syn


def build_potential_usernames_combos(
    token_list1,
    token_list2,
    delimeter_strategies=['default'],
    lettering_strategies=['default']
  ):
  potential_usernames = []

  potential_usernames_est_length = \
    len(token_list1) * \
      len(token_list2) * \
        len(delimeter_strategies) * \
          len(lettering_strategies)
  
  print(f'est. potential usernames: {potential_usernames_est_length}')
  next_percentage_point = 1

  for token1 in token_list1:
    for token2 in token_list2:
      if token1 == token2:
        continue
      for delimeter_strategy in delimeter_strategies:
        for lettering_strategy in lettering_strategies:

          potential_username = link_two_tokens(
            token1,
            token2,
            delimiter_strategy=delimeter_strategy,
            lettering_strategy=lettering_strategy
          )

          processed_potential_username = process_potential_username(potential_username)

          if processed_potential_username is not None \
            and processed_potential_username not in potential_usernames:
              potential_usernames.append(processed_potential_username)
          
          if len(potential_usernames) == round(potential_usernames_est_length / 100) * next_percentage_point:
            print(f'{next_percentage_point}% complete. ({len(potential_usernames)} usernames generated)')
            next_percentage_point += 1


def process_potential_username(potential_username: str):
  stripped_username = potential_username.strip()
  
  for invalid_username_character in INVALID_USERNAME_CHARACTERS:
    if invalid_username_character in stripped_username:
      return None
  
  return stripped_username


def link_two_tokens(
    token1,
    token2,
    delimiter_strategy='default',
    lettering_strategy='default'
  ):
  
  delimeter = build_delimiter(delimiter_strategy)
  token1 = modify_token1(token1, lettering_strategy)
  token2 = modify_token2(token2, lettering_strategy)

  return f'{token1}{delimeter}{token2}'


def build_delimiter(delimiter_strategy):
  if type(delimiter_strategy) is list:
    return ''.join([build_single_delimiter(x) for x in delimiter_strategy])
  elif type(delimiter_strategy) is str:
    return build_single_delimiter(delimiter_strategy)
  else:
    raise Exception('delimiter strategy must be a string or a list of strings')


def build_single_delimiter(delimeter_strategy):
  return DELIMETER_STRATEGY_MAP.get(delimeter_strategy, '')


def modify_token1(token, lettering_strategy):
  if 'first_token' in lettering_strategy:
    if lettering_strategy in LETTERING_STRATEGY_MAP.keys():
      modify = LETTERING_STRATEGY_MAP.get(lettering_strategy)
      return modify(token)
  return token


def modify_token2(token, lettering_strategy):
  if 'last_token' in lettering_strategy:
    if lettering_strategy in LETTERING_STRATEGY_MAP.keys():
      modify = LETTERING_STRATEGY_MAP.get(lettering_strategy)
      return modify(token)
  return token


def get_unique_synonyms(seed):
  path_to_synonyms = f'data/synonyms/{seed}/unique.txt'

  if not exists(path_to_synonyms):
    print(f'we have not built keywords for seed: {seed}')
    build_keywords_using_synonyms(seed)

  return get_from_file(path_to_synonyms).split('\n')