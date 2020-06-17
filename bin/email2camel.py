#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, sys, re, json, codecs, logging, stringcase

from collections import OrderedDict

from Argumental.Argue import Argue
from Spanners.Squirrel import Squirrel
from Perdy.pretty import prettyPrint
from Baubles.Logger import Logger

args = Argue()
squirrel = Squirrel()
logger = Logger()

#_________________________________________________________________
@args.argument(short='v', flag=True)
def verbose(): return False

@args.argument(short='i', help='read from file, defaults to stdin')
def input(): return

@args.argument(short='o', help='putput to file, defaults to stdout')
def output(): return

#_________________________________________________________________
@logger.debug
def main():
	'''
	test script to show logging working
	'''

	args.parse() #'-v'.split())
	if verbose():
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	header_pattern = re.compile('^(from|date|to|cc|subject):\s(.*)$',re.IGNORECASE)
	mail_pattern = re.compile('([^<]*)<([^>]*)>')

	if input():
		_input = open(input())
	else:
		_input = sys.stdin
		
	if output():
		_output = open(output(),'w')
	else:
		_output = sys.stdout

	for _line in _input.read().split('\n'):
		_line = _line.replace('\'','').replace('"','')
		m = header_pattern.match(_line)
		if not m: continue
		(prefix, tail) = tuple(m.groups())
		_output.write('%s:\n'%prefix)

		if '@' not in tail:
			_output.write('\t%s\n'%tail)
			continue

		tail = tail.replace(',',';')
		
		for _part in tail.split('; '):
			m = mail_pattern.match(_part)
			if not m: continue
			
			(name,email) = tuple(m.groups())
			name = name.strip()
			email = email.strip()
			if '@' in name:
				name = name.split('@')[0]
			if '.' in name:
				name = ' '.join(name.split('.'))
			name = name.lower()
			name = stringcase.titlecase(name)
			email = email.lower()
			fixed = '\t%s <%s>\n'%(name,email)
			_output.write(fixed)
	
	if output():
		_output.close()

#_________________________________________________________________
if __name__ == '__main__': main()
	
	
