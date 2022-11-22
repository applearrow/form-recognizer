import json

from termcolor import colored

def compare_results (images, correct_values_json, results_folder = 'results'):
  
  matches = {}
  fiels_to_compare = [ 'MerchantName', 'Total', 'TransactionDate' ]
  for field in fiels_to_compare:
    matches[field] = 0

  with open(correct_values_json) as json_file:
    correct_values = json.load(json_file)
    num_correct_values = len(images)
 
    for result in correct_values:
      imageFile = result['ImageFile']
      if imageFile in images:
        with open(f"{results_folder}/{imageFile}.json", 'r') as extracted_values_json:
          extracted_values = json.load(extracted_values_json)
          for field in fiels_to_compare:
            try: 
              correct = result[field]
              extracted = extracted_values[field]
              if extracted == correct:
                matches[field] += 1
              else:
                print (colored(f'{imageFile}:{field}: "{extracted}" <> "{correct}"', 'red'))  
            except:
              pass

  print (matches)
  print ([matches[x]/num_correct_values for x in matches], num_correct_values)
        
