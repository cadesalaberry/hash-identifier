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

def get_name(l):
  # Extracts "FCS16" from "def FCS16():"
  return re.match('def (\w+)\(\)\:', l).group(1)

def get_sample(l):
  # Extracts "4607" from "hs='4607'"
  return re.match('.+hs=\'(.+)\'', l).group(1)

def get_id(l):
  # Extracts "101020" from "jerar.append("101020")"
  return re.match('.+jerar.append\(\"(.+)\"\)', l).group(1)


def extract_boolean(variable, line):

  if variable + '==True' in line:
    return True
  elif variable + '==False' in line:
    return False
  else:
    raise ValueError('Confusing boolean for ' + variable)



def get_format_rules(line):
  re.match('.+(if len\(hash\)==len\(hs\)).+', line).group(1)

  format_rules = {}

  booleans_to_scan = [
    ('hash.isdigit()', 'digit'),
    ('hash.isalpha()', 'alpha'),
    ('hash.isalnum()', 'alnum')
  ]

  regex_to_scan = [
    ('.+hash\[0:\d+\]\.find\(\'(.+)\'\)==0.+', 'starts_with')
  ]

  # Extracts boolean rules
  for variable, name in booleans_to_scan:
    try:
      if variable in line:
        v = extract_boolean(variable, line)
        print variable, ":", v
        format_rules.update({name: v})

    except ValueError:
      pass

  # Extracts regex rules
  for regex_rule, name in regex_to_scan:
    try:
      v = re.match(regex_rule, line).group(1)
      if v:
        print name, ":", variable, ":", v
        format_rules.update({name: v})

    except AttributeError:
      pass

  return format_rules


def scan(line, i=-1):

  try:
    n = get_name(line)
    dic.append({'name': n})
    print i, "\tName:", n

  except AttributeError:
    pass

  try:
    s = get_sample(line)
    dic[-1]['sample'] = s
    print i, "\t\tSample:", s

    dic[-1]['size'] = len(s)
    print i, "\t\tSize:", len(s)

  except AttributeError:
    pass

  try:
    r = get_format_rules(line)
    dic[-1]['rules'] = r
    print i, "\t\tRules:", len(r)

  except AttributeError:
    pass

  try:
    hash_id = get_id(line)
    dic[-1]['id'] = hash_id
    print i, "\t\tHash ID:", hash_id

  except AttributeError:
    pass

def main():

  with open('sample') as f:
    content = f.readlines()

    for i, line in enumerate(content):
      scan(line, i)

  print json.dumps(dic, sort_keys=True, indent=2)



if __name__ == '__main__':
  main()
