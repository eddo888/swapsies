#!/usr/bin/env bash

bin/ref2type.py xsd/cod.xsd Document
pyxbgen xsd/cod.types.xsd
mv binding.py Swapsies/CloudOutlinerXSD.py

pyxbgen xsd/opml.xsd
mv binding.py Swapsies/OutlineXSD.py
