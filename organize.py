#!/usr/bin/env python3

import os, re, sys

from Perdy.parser import printXML
from GoldenChild.xpath import *


#_____________________________________________________________
def process_node(xml, node):
	print('%s'%node.name)
	nodes = dict()
	for child in getElements(xml.ctx, 'xs:element', node):
		name = getAttribute(child, 'name')
		print('\t%s'%name)
		nodes[name] = child
		setAttribute(child, 'minOccurs','0')
		child.unlinkNode()
	for name in sorted(nodes.keys()):
		node.addChild(nodes[name])

#_____________________________________________________________
def process_file(file):
	print(file)
	
	xml = XML(*getContextFromFile(file, argsNS=[
		'xs="http://www.w3.org/2001/XMLSchema"',
	]))

	for element in getElements(xml.ctx, '//xs:sequence'):
		process_node(xml, element)

	if True:
		name = file
	else:
		name = '%s/.%s'%(
			os.path.dirname(file),
			os.path.basename(file),
		)
	
	with open(name, 'w') as output:
		printXML(str(xml.doc), output=output)


#_____________________________________________________________
def main():
	for file in sys.argv[1:]:
		process_file(file)
		

#_____________________________________________________________
if __name__ == '__main__': main()
