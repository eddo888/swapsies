#!/usr/bin/env bash

cp ../../eddo888/Outliner/xsd/cod.xsd xsd/
#perl -pe 's/xs:sequence>/xs:choice>/;s/<xs:choice>/<xs:choice minOccurs="0" maxOccurs="unbounded">/' -i xsd/cod.xsd 

bin/ref2type.py xsd/cod.xsd Document
pyxbgen xsd/cod.types.xsd
mv binding.py Swapsies/CloudOutlinerXSD.py

pyxbgen xsd/opml.xsd
mv binding.py Swapsies/OutlineXSD.py
