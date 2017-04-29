#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:	dia
import glob,re
from bs4 import BeautifulSoup
import treetaggerwrapper as tt
tagger = tt.TreeTagger(TAGLANG='de', TAGDIR='/home/dia/Downloads/dhtools/TreeTagger/') # , TAGOPT = '-quiet'

# ################################# #
# 		FUNCTIONS
# ################################# #
# TAGGER
def tag(inp):
	""" TAKES str AND OUTPUTS tagged tt-list """
	return tt.make_tags(tagger.tag_text(inp))
# XML-CONSTRUCTOR
def makexml(inp):
	""" TAKES list of str AND OUTPUTS xml-SOUP """
	choice=input("Do you want to show the treetagger calculation? (y)")
	xml=BeautifulSoup("<MAIN></MAIN>", "lxml-xml")
	chapnum=0
	for chapter in inp:
		xml.MAIN.append( xml.new_tag("CHAPTER") )
		for w in tag(chapter):
			try:
				if w[0]!="replaced-dns":
					nt = xml.new_tag("w", word=w[0], pos=w[1], lemma=w[2] )
					nt.string = w[0]
					xml.find_all("CHAPTER")[chapnum].append( nt )
			except IndexError:
				url= re.search('text="(.+?)"', w[0]).group(1)
				nt = xml.new_tag("w", word=url, href=url)
				nt.string = url
				xml.find_all("CHAPTER")[chapnum].append( nt )
			if choice=="y" or "Y":
				print(w)
		chapnum+=1
	return xml

# ################################# #
# 		MAIN
# ################################# #
# READ & WRITE FILES
def main():
	""" TAKES ALL .txt-files in same folder AND MAKES .xml-files """
	files = glob.glob('*.txt')
	for filename in files:
		with open(filename, "r", encoding="utf-8") as fhread:
			print('read  "'+filename+'"')
			text=re.split("\n\n\n\n",fhread.read()) # returns list ### CHAPTERS DIVIDED BY 4 newlines!
			newfilename = filename[:-4]+".xml"
			with open(newfilename, "w", encoding="utf-8") as fhwrite:
					print('calculate…')
					fhwrite.write( makexml(text).prettify() )
					print('write "'+newfilename+'"')
	print("finished")
