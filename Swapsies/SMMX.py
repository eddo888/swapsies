#!/usr/bin/env python3

import os, re, sys
from zipfile import ZipFile
from GoldenChild.xpath import *
from Perdy.parser import printXML
from Spanners.IdentityCache import IdentityCache

empty='''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE simplemind-mindmaps>
<simplemind-mindmaps generator="SimpleMindWin32" gen-version="2.2.0" doc-version="3">
    <mindmap>
        <meta>
            <guid guid="7077E873F4AB4B1DBAED22AA98B10293"/>
            <title text="SimpleMind"/>
            <style key="system.basic-chart"/>
            <auto-numbering style="disabled"/>
            <scrollstate zoom="100" x="628" y="233"/>
            <selection guid="6iDcrhzb4ka0Ag540bwc8g" type="node" id="0"/>
            <main-centraltheme id="0"/>
        </meta>
        <topics>
            <topic id="0" parent="-1" guid="6iDcrhzb4ka0Ag540bwc8g" x="536.67" y="333.33" text="SimpleMind" textfmt="plain">
                <layout mode="list" direction="auto" flow="auto"/>
            </topic>
        </topics>
        <relations/>
    </mindmap>
</simplemind-mindmaps>
'''

class SMMX:
	'''
	simple xml wrapper around the Simple Mind SMMX file format
	'''
	
	def __init__(self):
		self.ids = IdentityCache()
		self.name = 'document/mindmap.xml'
		self.last = 0


	def load(self, file):
		self.file = file
		print(f'< {file}')

		if file:
			zf = ZipFile(file)
			with zf.open(self.name) as input:
				xml = input.read().decode('UTF-8')
				self.mindmap = XML(*getContextFromString(xml))
		else:
			self.mindmap = XML(*getContextFromString(empty))
			
		for topic in getElements(self.mindmap.ctx, 'topic', self.topics):
			id = int(getAttribute(topic, 'id'))
			if id > self.last:
				self.last = id


	@property
	def topics(self):
		return getElement(self.mindmap.ctx, "/simplemind-mindmaps/mindmap/topics")

	
	@property
	def root(self):
		return getElement(self.mindmap.ctx, "topic[@id='0']", self.topics)


	def task(self, node, tipe=None):
		'''
		oneof=['checkbox', 'rollup'])
		'''
		
		if tipe == 'rollup':
			setAttribute(node, 'checkbox-mode', 'roll-up-progress')
			other = getAttribute(node, 'checkbox')
			if other:
				other.unlinkNode()
				other.freeNode()

		if tipe == 'checkbox':
			setAttribute(node, 'checkbox', 'True')
			other = getAttribute(node, 'checkbox-mode')
			if other:
				other.unlinkNode()
				other.freeNode()

				
	def add(self, name, text=None, parent=None):
		child = addElement(self.mindmap.doc, 'topic', self.topics)
		self.last += 1
		setAttribute(child, 'id', f'{self.last}')

		if not parent: parent = self.root
		pid = getAttribute(parent, 'id')
		setAttribute(child, 'parent', f'{pid}')
		
		guid = self.ids.get(f'smmx_{self.last}')
		setAttribute(child, 'guid', guid)
		
		setAttribute(child, 'text', name)
		setAttribute(child, 'textfmt', 'plain')

		if text: addElementText(self.mindmap.doc, 'note', text, child)

		return child

	
	def link(self, source, target):
		pass
	

	def save(self, file=None):
		file = file or self.file
		print(f'> {file}')
		if file:
			zf = ZipFile(file, 'w')
			with zf.open(self.name, 'w') as output:
				xml = str(self.mindmap.doc)
				output.write(xml.encode('UTF-8'))
		self.ids.save()
		



