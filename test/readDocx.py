#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, sys, re

from docx import Document
from docx.shared import Inches

document = Document('_test.cod.docx')

for paragraph in document.paragraphs:
	print(paragraph.text)
	
	for run in paragraph.runs:

		for key in dir(run):
			if key.startswith('_'):
				continue
			print('\t', key, getattr(run, key))

		
