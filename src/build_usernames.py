from src.build_keywords import build_keywords_using_synonyms, get_adjectives, get_from_synonyms
from src.utils.utils import get_from_file
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

LETTERING_STRATEGIES = LETTERING_STRATEGY_MAP.keys()


def build_usernames(topic):
  potential_usernames = []

  synonyms = get_unique_synonyms(topic)
  adjectives = get_adjectives()

  # build usernames with 1 synonym
  # potential_usernames.extend(synonyms)

  # build usernames with 2 synonyms + all combos of delimeters, synonyms
  # [syn] [del] [syn]
  for synonym1 in synonyms:
    print('syn1: {}'.format(synonym1))
    for synonym2 in synonyms:
      if synonym1 == synonym2: pass
      for delimeter_strategy in DELIMETER_STRATEGIES:
        # for lettering_strategy in LETTERING_STRATEGIES:
          potential_username = link_two_tokens(
            synonym1,
            synonym2,
            delimeter_strategy,
            # lettering_strategy
          )
          if ' ' not in potential_username.strip() and '\'' not in potential_username:
            potential_usernames.append(potential_username.strip())
  
  # [syn] [del] [adj]
  for synonym in synonyms:
    for adjective in adjectives:
      for delimeter_strategy in DELIMETER_STRATEGIES:
        # for lettering_strategy in LETTERING_STRATEGIES:

          potential_username1 = link_two_tokens(
            synonym,
            adjective,
            delimeter_strategy,
            # lettering_strategy
          )
          potential_username2 = link_two_tokens(
            adjective,
            synonym,
            delimeter_strategy,
            # lettering_strategy
          )

          potential_usernames.append(potential_username1)
          potential_usernames.append(potential_username2)
  
  return potential_usernames

  # Coming soon
  # build usernames with 3 synonyms + all combos of delimeters, synonyms
    # syn [del] syn [del] syn
    # syn [del] syn [del] adj
    # syn [del] adj [del] syn
    # adj [del] syn [del] syn
  pass


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