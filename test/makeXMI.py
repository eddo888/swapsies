#!/usr/bin/env python3

import sys, os, re

sys.path.insert(0, '..')

from Perdy.parser import printXML
from Swapsies.xmi import XMI

xmi = XMI('sameo')

fundamental_package = xmi.makePackage('Fundamentals', xmi.modelNS)
fundamental_diagram = xmi.makeClassDiagram('Fundamentals', fundamental_package)

base_types = dict() # name: id

for base_type in ['text','number','datetime']:
	_base_type = xmi.makeClass(base_type, fundamental_package, uid=base_type)
	xmi.addDiagramClass(_base_type, fundamental_diagram)
	xmi.makeStereotype('BaseType', _base_type)
	base_types[base_type] = _base_type

children_package = xmi.makePackage('Children', fundamental_package)
xmi.addDiagramClass(children_package, fundamental_diagram)

xmi.makeDependency(children_package, fundamental_package, xmi.modelNS)

_the_type = xmi.makeClass('the_type', children_package)
xmi.makeAttribute('the_atrr',base_types['text'], 'value', _the_type)

with open(sys.argv[0]+'.xmi', 'w') as _output:
	printXML(str(xmi.doc), output=_output, colour=False)
