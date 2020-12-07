#!/usr/bin/env python3

import sys, os, re

sys.path.insert(0, '..')

from Perdy.parser import printXML
from Swapsies.xmi import XMI

xmi = XMI('sameo')

classes = xmi.makePackage('Fundamentals', xmi.modelNS)
diagram = xmi.makeClassDiagram('Fundamentals', classes)

base_types = dict() # name: id

for base_type in ['text','number','datetime']:
	_base_type = xmi.makeClass(base_type, classes, uid=base_type)
	xmi.addDiagramClass(_base_type, diagram)
	xmi.makeStereotype('BaseType', _base_type)
	base_types[base_type] = _base_type

_classes = xmi.makePackage('Children', classes)
xmi.addDiagramClass(_classes, diagram)

_the_type = xmi.makeClass('the_type', _classes)
xmi.makeAttribute('the_atrr',base_types['text'], 'value', _the_type)

with open(sys.argv[0]+'.xmi', 'w') as _output:
	printXML(str(xmi.doc), output=_output, colour=False)
