#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:	dia

import os,sys,glob,re,itertools
from collections import Counter
from bs4 import BeautifulSoup
import con_TXT2XML as txt2xml

if not glob.glob('*.xml'):
	txt2xml.main()

with open("op_NundN.tsv", "w", encoding="utf-8") as fh:
	fh.write("Source\tTarget\tType\n")
with open("op_NundN_Nwordlist.tsv","w", encoding="utf-8") as fh:
	fh.write("Id\tDegree\n")
xmlfiles = glob.glob('*.xml')
for ipfilename in xmlfiles:
	with open(ipfilename, "r", encoding="utf-8") as fh:
		print("Calculating xml-file…")
		xml=BeautifulSoup(fh.read(), "lxml-xml")
		Nset=set()
		for word in xml.find_all("w",word="und"):
			if re.match("^N", word.find_previous_sibling("w")['pos']) and re.match("^N", word.find_next_sibling("w")['pos']):
				source=re.search("\w+",word.find_previous_sibling("w")['lemma']).group(0)
				target=re.search("\w+",word.find_next_sibling("w")['lemma']).group(0)
				with open("op_NundN.tsv","a", encoding="utf-8") as fhwrite:
					op=[source,target,"Undirected"]
					fhwrite.write("\t".join(op)+"\n")

				Nset.update([re.search("\w+",word.find_previous_sibling("w")['lemma']).group(0), re.search("\w+",word.find_next_sibling("w")['lemma']).group(0)])
			
		wlist=list()	
		for w in xml.find_all("w", lemma=True, word=re.compile("\w+")):
			wlist.append( re.search("\w+",w['lemma']).group(0) )
		allwordcount=Counter(wlist)
		for n in Nset:
			with open("op_NundN_Nwordlist.tsv","a", encoding="utf-8") as fhwrite:
				fhwrite.write( n+"\t"+str(allwordcount[n])+"\n" )
				

