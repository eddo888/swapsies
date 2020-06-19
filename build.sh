#!/usr/bin/env bash

#cp ../../eddo888/Outliner/xsd/cod.xsd xsd/
bin/ref2type.py xsd/cod.xsd Document
./organize.py xsd/cod.types.xsd

pyxbgen xsd/cod.types.xsd
mv binding.py Swapsies/CloudOutlinerXSD.py

pyxbgen xsd/opml.xsd
mv binding.py Swapsies/OutlineXSD.py
