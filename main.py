from src.build_usernames import build_usernames

if __name__ == '__main__':
  potential_usernames = build_usernames('money')
  print(len(potential_usernames))