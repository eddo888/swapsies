#!/usr/bin/env python3

import os, re, sys, PyPDF2

with open(sys.argv[1], 'rb') as input:
	reader = PyPDF2.PdfFileReader(input)
	print(reader.numPages)
	page = reader.getPage(0)
	print(page.extractText())

	
