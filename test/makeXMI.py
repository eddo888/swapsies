#!/usr/bin/env python3

import sys, os, re

sys.path.insert(0, '..')

from Perdy.parser import printXML
from Swapsies.xmi import XMI

xmi = XMI(name='TEST')

with open(sys.argv[0]+'.xmi', 'w') as _output:
	printXML(str(xmi.doc), output=_output, colour=False)
