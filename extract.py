#!/usr/bin/env python
"""
encoding: utf-8
Hash Identifier v1.2
By C4Labz (From Zion3R)
www.c4labz.com
"""

import re
import json

dic = []
algorithms = {}

# Extracts "FCS16" from "def FCS16():"
def get_name(l):
  return re.match('def (\w+)\(\)\:', l).group(1)

# Extracts "4607" from "hs='4607'"
def get_sample(l):
  return re.match('.+hs=\'(.+)\'', l).group(1)

# Extracts "101020" from "jerar.append("101020")"
def get_id(l):
  return re.match('.+jerar.append\(\"(.+)\"\)', l).group(1)

# Returns a boolean from a line like :
# "... and hash.isdigit()==False and ..."
def extract_boolean(variable, line):

  if variable + '==True' in line:
    return True
  elif variable + '==False' in line:
    return False
  else:
    raise ValueError('Confusing boolean for ' + variable)


# Extracts boolean rules from a list like :
# booleans_to_scan = [('hash.isdigit()', 'digits_only')]
def extract_booleans(line, booleans_to_scan):

  rules = {}

  for variable, name in booleans_to_scan:
    try:
      if variable in line:

        v = extract_boolean(variable, line)

        rules[name] = v

    except ValueError:
      pass

  return rules


def extract_regexes(line, regexes_to_scan):

  rules = {}

  # Extracts regex rules
  for regex_rule, name in regexes_to_scan:
    try:
      v = re.match(regex_rule, line).group(1)
      if v:
        # Turns the value into an int if possible
        try:
          v = int(v)
        except ValueError:
          pass

        rules[name] = v

    except AttributeError:
      pass

  return rules


def get_format_rules(line):

  # Returns an AttributeError if not a format_rule
  re.match('.+(if len\(hash\)==len\(hs\)).+', line).group(1)

  format_rules = {}

  booleans_to_scan = [
    ('hash.isdigit()', 'digits_only'),
    ('hash.isalpha()', 'letters_only'),
    ('hash.isalnum()', 'alnumeric'),
    ('hash.islower()', 'lowercase')
  ]

  regex_to_scan = [
    ('.+hash\[0:\d+\]\.find\(\'(.+)\'\)==0.+', 'starts_with'),
    ('.+hash\[(\d+):\d+\]\.find\(\':\'\)==0.+', 'colon_index')
  ]

  booleans = extract_booleans(line, booleans_to_scan)
  format_rules.update(booleans)


  regexes = extract_regexes(line, regex_to_scan)
  format_rules.update(regexes)

  return format_rules


def scan(line, i=-1):

  try:
    n = get_name(line)
    dic.append({'name': n})

  except AttributeError:
    pass

  try:
    s = get_sample(line)
    dic[-1]['sample'] = s
    dic[-1]['size'] = len(s)

  except AttributeError:
    pass

  try:
    r = get_format_rules(line)
    dic[-1]['rules'] = r

  except AttributeError:
    pass

  try:
    hash_id = get_id(line)
    dic[-1]['id'] = hash_id

  except AttributeError:
    pass

def main():

  # with open('sample') as f:
  with open('Hash_ID_v1.1.py') as f:
    content = f.readlines()

    for i, line in enumerate(content):
      scan(line, i)

  readable_json = json.dumps(dic, sort_keys=True, indent=2)

  print readable_json

  with open('hash-identifier.db.json', 'w') as o:
    o.write(readable_json)

  with open('hash-identifier.db.min.json', 'w') as o:
    json.dump(dic, o)

if __name__ == '__main__':
  main()
