#!/usr/bin/env python3

import sys, os, re

sys.path.insert(0, '..')

from Perdy.parser import printXML
from Swapsies.xmi import XMI

xmi = XMI()

classes = xmi.makePackage('Fundamentals', xmi.modelNS)
diagram = xmi.makeClassDiagram('Fundamentals', classes)

for base_type in ['text']:
	_base_type = xmi.makeClass(base_type, classes, uid=base_type)
	xmi.addDiagramClass(_base_type, diagram)
	xmi.makeStereotype('BaseType', _base_type)
	
_classes = xmi.makePackage('Children', classes)
xmi.addDiagramClass(_classes, diagram)

_the_type = xmi.makeClass('the_type', _classes)

with open(sys.argv[0]+'.xmi', 'w') as _output:
	printXML(str(xmi.doc), output=_output, colour=False)
