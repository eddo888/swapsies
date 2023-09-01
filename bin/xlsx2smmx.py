#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, json, pandas

if os.path.dirname(sys.argv[0]) == '.':
	sys.path.insert(0,'..')

from openpyxl import load_workbook
from GoldenChild.xpath import *
from Perdy.parser import printXML
from Argumental.Argue import Argue
from Swapsies.SMMX import SMMX

args = Argue()

@args.command(single=True)
class Converter:

	@args.property(short='v', flag=True, help='verbose mode')
	def verbose(self): return
	
	@args.operation
	@args.parameter(name='xlsx', short='x', help='excel file to convert to SMMX')
	@args.parameter(name='input', short='i', help='source SMMX to populate')
	@args.parameter(name='output', short='o', help='output SMMX file')
	@args.parameter(name='headers', short='H', flag=True, help='include headers')
	def toSMMX(self, xlsx=None, input=None, output=None, headers=False):
		'''
		create a nested mind map based on columns in excel
		'''
		
		smmx = SMMX()
		smmx.load(input)
		setAttribute(smmx.root, 'text', xlsx)
		setAttribute(smmx.root, 'checkbox-mode', 'roll-up-progress')
		
		
		def dig(pf, mm, indent='  '):
			k = list(pf.columns)
			
			for i in pf[k[0]].unique():
				if self.verbose:
					print(f'{indent}{i}')

				text = str(i)
				if headers:
					text = f'{k[0]}: {text}'
					
				child = smmx.add(text, parent=mm)

				if len(k) > 1:
					smmx.task(child, tipe='rollup')
					qf = pf[pf[k[0]]==i][k[1:]].reset_index(drop=True)
					dig(qf, child, indent=f'{indent}  ')
				else:
					smmx.task(child, tipe='checkbox')
				
					
		wb = load_workbook(xlsx)
		for sheet in wb:
			
			if self.verbose:
				print(sheet.title)

			text = sheet.title
			if headers:
				text = f'Sheet: {text}'
				
			parent = smmx.add(text)
			setAttribute(parent, 'checkbox-mode', 'roll-up-progress')

			df = pandas.read_excel(xlsx, sheet_name=sheet.title).reset_index(drop=True)
			dig(df, parent)

		if self.verbose:
			printXML(str(smmx.topics), colour=True)

		smmx.save(output)
	

if __name__ == '__main__': args.execute()


