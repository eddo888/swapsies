#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, os, json, logging, arrow, codecs

sys.path.append('..')

from uuid import uuid4

from Baubles.Logger import Logger
from Perdy.pretty import prettyPrint
from Perdy.parser import printXML
from Perdy.pyxbext import directory
from Argumental.Argue import Argue

logger = Logger()
args = Argue()

for name in [
	'pyxb.binding.content',
	'pyxb.binding.basis',
]:
	logging.getLogger(name).setLevel(logging.ERROR)

logger.setLevel(logging.INFO)

from Swapsies.CloudOutlinerXSD import *


#____________________________________________________________
@args.command(single=True)
class COD(object):


	#........................................................
	def __init__(self):
		'''
		setup constructor with lookup lists
		'''
		self.xcolours = {
			'Black': '\033[30m',
			'Red': '\033[31m',
			'Green': '\033[32m',
			'Orange': '\033[33m',
			'Blue': '\033[34m',
			'Purple': '\033[35m',
			'Teal': '\033[36m',
			'White': '\033[37m',
			'Off': '\033[0m',
		}

		self.colours = {
			0: 'White',
			5: 'Blue',
			4: 'Green',
			2: 'Red',
			3: 'Orange',
			6: 'Purple',
		}

		self.xfonts = {
			'bold': '\033[1m',
			'italics': '\033[3m',
			'underline': '\033[4m',
			'strikeout': '\033[9m',
			'normal': '\033[0m',
		}

		self.fonts = {
			0: 'normal',
			8: 'bold',
			2: 'underline',
			1: 'strikeout',
			4: 'italics',
		}

		self.claszes = {
			Properties: 'DMDocument',
			ChildItem: 'DMDocumentInnerObject',
			context: 'DMDocumentInnerObject',
			title: 'NSTaggedPointerString',
			note: '__NSCFConstantString',
			password: '__NSCFConstantString',
			notes: '__NSCFString',
			color: '__NSCFNumber',
			completionState: '__NSCFNumber',
			defaultColor: '__NSCFNumber',
			defaultFontStyle: '__NSCFNumber',
			fontSize: '__NSCFNumber',
			fontStyle: '__NSCFNumber',
			hideCheckedEnements: '__NSCFNumber',
			hideUncheckedEnements: '__NSCFNumber',
			isExpanded: '__NSCFNumber',
			isGroup: '__NSCFNumber',
			lastModificationTime: '__NSCFNumber',
			markColor: '__NSCFNumber',
			numerationStyle: '__NSCFNumber',
			readOnly: '__NSCFNumber',
			resizebleLineForTextSize: '__NSCFNumber',
			showCheckBox: '__NSCFNumber',
			showNotesOnlyForSelectedRow: '__NSCFNumber',
		}

		self.sruoloc = dict()
		for x, y in self.colours.items():
			self.sruoloc[y] = x

		self.stonf = dict()
		for x, y in self.fonts.items():
			self.stonf[y] = x


	#........................................................
	@logger.debug
	def f(self, clasz, *args, **kwargs):
		'''
		constructor with className
		'''
		obj = clasz(*args, **kwargs)
		if clasz in list(self.claszes.keys()):
			obj.className = self.claszes[clasz]
		return obj


	#........................................................
	def __clean(self, text):
		while '\u2013' in text:
			text = text.replace('\u2013', '"')
		return text


	#........................................................
	@logger.info
	@args.operation
	def diagnostics(self):
		'''
		print out diagnostics
		'''
		print(json.dumps(dict(
			sruoloc=self.sruoloc,
			stonf=self.stonf, ), indent=4))


	#........................................................
	@logger.debug
	def __show(self, childItem, indent='', checkboxes=False, shownotes=False):
		'''
		show a single item
		'''
		font = childItem.fontStyle[0].value()
		colour = childItem.color[0].value()
		state = childItem.completionState[0].value() == 3
		if checkboxes:
			checked = '[x] ' if state else '[ ] '
		else:
			checked = ''
		_colour = self.xcolours[self.colours[colour]] or ''
		_font = self.xfonts[self.fonts[font]] or ''
		print('%s%s%s%s%s%s' % (
			indent, _font, _colour, checked,
			childItem.title[0].value(), self.xcolours['Off'], )
		)
		
		if childItem.notes:
			if shownotes:
				note = childItem.notes[0].value()
				if note != '(null)':
					print('%s%s  "%s"%s' % (
						self.xcolours['Teal'], '%s  ' % indent
						if checkboxes else indent, note,
						self.xcolours['Off'],
					))

		for grandChild in childItem.ChildItem:
			self.__show(
				grandChild,
				indent='%s  ' % indent,
				checkboxes=checkboxes,
				shownotes=shownotes
			)
			

	#........................................................
	@logger.debug
	def __convert(self, file, cod, checkboxes=False, shownotes=False):
		'''
		show the cod file
		'''
		m = cod.Properties[0].lastModificationTime[0].value()
		u = arrow.get(m)
		a = u.to('local').format('YYYY-MM-DD HH:mm:ss SSS Z')
		t = cod.Properties[0].title[0].value()
		print('%s -> "%s" => %s' % (file, t, a))
		children = cod.Properties[0].context[0].ChildItem
		for childItem in children:
			self.__show(childItem, checkboxes=checkboxes, shownotes=shownotes)
			

	#........................................................
	@logger.debug
	@args.operation
	@args.parameter(name='checkboxes', short='c', flag=True, help='show checkboxes')
	@args.parameter(name='shownotes', short='n', flag=True, help='show text notes')
	@args.parameter(name='blackAndWhite', short='b', flag=True, help='black and white')
	def cod2text(self,
		file,
		checkboxes=False,
		shownotes=False,
		blackAndWhite=False
	):
		'''
		load a cod file and display
		'''
		if blackAndWhite:
			for key in list(self.xcolours.keys()):
				self.xcolours[key] = ''
			for key in list(self.xfonts.keys()):
				self.xfonts[key] = ''

		with open(file) as input:
			cod = CreateFromDocument(input.read())
			self.__convert(file, cod, checkboxes=checkboxes, shownotes=shownotes)
		return


	#........................................................
	@logger.debug
	def __node(self,
		xmi,
		node,
		UseCases=[],
		Systems=[],
		seperator='\s+\=\s+',
		indent='',
		constructor=None,
		parent=None
	):
		title = self.__clean(node.title[0].value())
		note = None
		if node.notes and len(node.notes):
			note = self.__clean(node.notes[0].value())
		else:
			parts = re.compile(seperator).split(title)
			if len(parts) > 1:
				title = parts[0]
				note = ''.join(parts[1:])

		print('%s%s:' % (indent, title))
		if note:
			print('%s  "%s"' % (indent, note))

		if constructor:
			child = constructor(title, parent)
			if note and len(note):
				xmi.addDocumentation(note, child)
			return child

		diagram = None
		if title in UseCases:
			parent = xmi.makePackage(title, parent)
			diagram = xmi.makeUseCaseDiagram(title, parent)
			constructor = xmi.makeUseCase

		if title in Systems:
			parent = xmi.makePackage(title, parent)
			diagram = xmi.makeClassDiagram(title, parent)
			constructor = xmi.makeComponent

		for child in node.ChildItem:
			item = self.__node(
				xmi,
				child,
				UseCases=UseCases,
				Systems=Systems,
				seperator=seperator,
				indent='%s  ' % indent,
				constructor=constructor,
				parent=parent)
			if diagram:
				xmi.addDiagramClass(item, diagram)


	#........................................................
	@logger.debug
	def __createClass(self, clasz, *args, **kwargs):
		'''
		constructor with className
		'''
		obj = clasz(*args, **kwargs)
		if clasz in list(self.claszes.keys()):
			obj.className = self.claszes[clasz]
		return obj


	#........................................................
	@logger.debug
	def __addChild(self,
		heading,
		parent,
		colour='White',
		font='normal',
		note=None,
		checked=False
	):
		'''
		add a child to a parent
		'''
		if colour not in list(self.sruoloc.keys()):
			colour = 'White'
		if font not in list(self.stonf.keys()):
			font = 'normal'

		f = self.f
		childItem = f(ChildItem, **dict(
			isExpanded=[f(isExpanded, 1)],
			isGroup=[f(isGroup, 1)],
			title=[f(title, heading)],
			completionState=[f(completionState, 3 if checked else 0)],
			color=[f(color, self.sruoloc[colour])],
			fontStyle=[f(fontStyle, self.stonf[font])],
			ID=[str(uuid4()).upper()],
			ChildItems=[f(ChildItems)],
			ChildItem=[], 
		))

		if note:
			childItem.notes = [f(notes, note)]

		parent.ChildItems[0].append(childItem.ID[0])
		parent.ChildItem.append(childItem)

		return childItem


	#........................................................
	@logger.debug
	def __createDocument(self, titlename):
		'''
		create an empty cod document
		'''
		n = arrow.now().timestamp
		f = self.f
		properties = f(Properties, **dict(
			isExpanded=[f(isExpanded, 1)],
			isGroup=[f(isGroup, 0)],
			title=[f(title, titlename)],
			password=[f(password, '(null)')],
			markColor=[f(markColor, 0)],
			note=[f(note, 'mynote')],
			context=[
				f(context, **dict(
					isExpanded=[f(isExpanded, 1)],
					isGroup=[f(isGroup, 1)],
					title=[f(title, 'mytitle')],
					completionState=[f(completionState, 0)],
					color=[f(color, 0)],
					fontStyle=[f(fontStyle, 0)],
					ID=[str(uuid4()).upper()],
					ChildItems=[f(ChildItems)],
					ChildItem=[], ))
			],
			fontSize=[f(fontSize, 14)],
			defaultFontStyle=[f(defaultFontStyle, 0)],
			defaultColor=[f(defaultColor, 0)],
			numerationStyle=[f(numerationStyle, 0)],
			lastModificationTime=[f(lastModificationTime, n)],
			showCheckBox=[f(showCheckBox, 1)],
			hideCheckedEnements=[f(hideCheckedEnements, 0)],
			hideUncheckedEnements=[f(hideUncheckedEnements, 0)],
			resizebleLineForTextSize=[f(resizebleLineForTextSize, 1)],
			showNotesOnlyForSelectedRow=[f(showNotesOnlyForSelectedRow, 0)],
			readOnly=[f(readOnly, 0)],
			ID=[str(uuid4()).upper()],
			ChildItems=[f(ChildItems)], ))

		cod = Document(
			version="2.0",
			Ext=['(null)'],
			Properties=[properties],
			BaseVersion=[
				f(BaseVersion, **dict(
					VersionNumber=[-1],
					Modified=[1],
					Ext=['(null)'],
					Properties=[properties], ))
			],
			VersionNumber=[0],
			Modified=[0], )

		return cod


	#........................................................
	@logger.debug
	@args.operation
	def dumper(self, file):
		'''
		create a sample test cod file for example purposes
		'''
		now = arrow.now().to('local').format('YYYY-MM-DD HH:mm:ss SSS')

		cod = self.__createDocument('my outline')
		root = cod.Properties[0].context[0]
		top = self.__addChild('created %s' % now, root)

		self.__addChild('checked', top, checked=True)
		self.__addChild('unchecked', top, checked=False)
		self.__addChild('noted', top, note='hello')

		colourChild = self.__addChild('colours', top)
		for colour in list(self.sruoloc.keys()):
			self.__addChild(colour, colourChild, colour=colour)

		fontChild = self.__addChild('fonts', top)
		for font in list(self.stonf.keys()):
			self.__addChild(font, fontChild, font=font)

		m = cod.Properties[0].lastModificationTime[0].value()
		u = arrow.get(m)
		a = u.to('local').format('YYYY-MM-DD HH:mm:ss SSS Z')
		t = cod.Properties[0].title[0].value()
		print('%s -> "%s" => %s' % (file, t, a))

		#directory(cod)

		with open(file, 'w') as output:
			printXML(cod.toxml(), output=output)

		return


#____________________________________________________________
if __name__ == '__main__': args.execute()


