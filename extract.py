#!/usr/bin/env python
"""
encoding: utf-8
Hash Identifier v1.2
By C4Labz (From Zion3R)
www.c4labz.com
"""

import re
import json

dic = [{}]
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

def get_format_rules(l):
	re.match('.+(if len\(hash\)==len\(hs\)).+', l).group(1)
	rules = {}

	if re.match('hash.isdigit()==False', l):
		rules['d'] = 0
		print "yo"
	elif re.match('hash.isdigit()==True', l):
		rules['d'] = 1

	return rules


def scan(line):

	try:
		n = get_name(line)
		dic.append({'n':n})

	except AttributeError:
		pass

	try:
		s = get_sample(line)
		dic[-1]['s'] = s

	except AttributeError:
		pass

	try:
		r = get_format_rules(line)
		dic[-1]['r'] = r

	except AttributeError:
		pass

	try:
	 	i = get_id(line)
	 	dic[-1]['i'] = i
	
	except AttributeError:
	 	pass

def main():

	

	with open('sample') as f:
		content = f.readlines()

		for line in content:
			scan(line)

	print json.dumps(dic, sort_keys=True, indent=2)



if __name__ == '__main__':
	main()
