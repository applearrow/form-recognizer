import os
from process_local_file import process_local_file
from decouple import config

def process_local_folder(folder: str = '08'):
  print(f'Processing {folder}...')

  for path in os.listdir(folder):
    fname = os.path.join(folder, path)
    if os.path.isfile(fname):
      process_local_file(fname)  

if __name__ == '__main__':
  folder = 'receipts'
  endpoint = config('FORM_RECOGNIZER_ENDPOINT')
  key = config('FORM_RECOGNIZER_KEY')
  print(f'KEY={key} ENDPOINT={endpoint}')
  process_local_folder(folder)
