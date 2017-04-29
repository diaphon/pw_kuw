#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:   dia

# window 300 words
# interconnect every word in this window

import os,sys,glob,re,itertools
from collections import Counter
from bs4 import BeautifulSoup

f="Waterhouse, Peter - Krieg und Welt.xml_"

def souper(filein):
    """ makes a soup of a xml-file """
    with open(filein, "r", encoding="utf-8") as fh:
        print("…")
        xml=BeautifulSoup(fh.read(), "lxml-xml")
        return xml

def windowgen(listin, windowsize):
    """ generates sliding window as list of list """
    l=list()
    [l.append( listin[i:i+windowsize] ) for i in range(len(listin)-windowsize+1)]
    return l

def printCounter(CounterO):
    """ prints Counter-object human-readable """
    for word,count in CounterO.most_common():
        print(count, word)

####################################
## # FUNCTIONS #####################

##################
## # COUNTERS # ##

def punctcount(filein):
    """ returns a Counter-object of all punctuationmarks """
    op=list()
    for pun in souper(filein).find_all(pos="$."):
        op.append(pun['word'])
    return Counter(op)

def lemmacount(filein):
    """ returns a Counter-object of input-regex """
    choice=input("Which word (lemma) would you like to search for? ")
    op=list()
    for word in souper(filein).find_all(lemma=re.compile(choice)):
        op.append(word['word'])
    return Counter(op)

def poscount(filein):
    """ returns Counter-object of POS-input """
    choice=input("Which STTS-POS would you like to search for (regex possible)? ")
    op=list()
    for pos in souper(filein).find_all(pos=re.compile("^"+choice)):
        op.append(pos['lemma'])
    return Counter(op)

## #          # ##
##################

##################
## #          # ##

def wordsaround(filein):
    """ returns Counter-object of words around input-word """
    choiceword=input("Which word would you like to search around? ")
    choicepos= input("Which STTS-POS tag should this words around be? ")
    choicewin= input("What should the word-window-size be? ")
    op=list()
    for word in souper(filein).find_all(word=re.compile(choiceword)):
        for n in range(0,int(choicewin)):
            try:
                nex = word.find_next_siblings("w")[n]
                if re.match(choicepos, nex['pos']):
                    op.append( nex['lemma'] )
            except:
                pass

            try:
                pre = word.find_previous_siblings("w")[n]
                if re.match(choicepos, pre['pos']):
                    op.append( pre['lemma'] )
            except:
                pass
    return Counter(op)


print()
file=input("INPUT FILENAME: ")
while True:
    print("""
        SELECT MODULE:
        1) punctcount
        2) lemmacount
        3) poscount
        4) wordsaround
        x) exit
    """)
    
    sel=input("WRITE NUMBER: ")
    if sel=="1":
        print( punctcount(file) )
    elif sel=="2":
        print( lemmacount(file) )
    elif sel=="3":
        print( poscount(file) )
    elif sel=="4":
        print( wordsaround(file) )
    elif sel=="x":
        break
    else:
        print("Please enter a number of the list")
