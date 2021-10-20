from threading import Thread

def get_from_file(file):
  f = open(file, 'r')
  data = f.read()
  f.close()
  return data

def write_to_file(file, content):
  f = open(file, 'a')
  f.write(f'{content}\n')
  f.close()

def run_concurrently_using_threads(fns_args: list[tuple[object, tuple]]):
  threads = []
  for fn, args in fns_args:
    threads.append(Thread(target=fn, args=args))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()

def create_file(file):
  f = open(file, 'a')
  f.close()
  return file