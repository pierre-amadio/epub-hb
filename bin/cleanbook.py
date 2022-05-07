#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup
from globals import *

inputFile=sys.argv[1]
outputDir=sys.argv[2]
m=re.search(".*\/(\S+)$",inputFile)
if m:
  shortName=m.group(1)
else:
  shortName=inputFile

print("Extracting book from %s"%shortName)

def createChapterHtml(chapter):
    chapterId=chapter["osisID"]
    
    data={}

    m=re.match("(\S+)\.(\d+)",chapterId)
    if not m:
        print("Cannot parse chapter",chapterId)
        sys.exit()
    bookId=m.group(1)
    bookName=bookAbbr[bookId]
    chapterNbr=m.group(2)
    data["id"]=chapterNbr
    data["nbr"]=chapterNbr

    data["verses"]=[]
    for verse in chapter.find_all("verse"):
        curVerse={}
        verseId=verse["osisID"]
        m=re.match("(\S+)\.(\d+)",verseId)
        if not m:
            print("Cannot parse verse",verseId)
            sys.exit()
        verseNbr=m.group(2)
        curVerse["nbr"]=verseNbr
        curVerse["content"]=""        
        for node in verse.find_all():
            if(node.name=="w"):
                word=node.string
                if(word.find("/")>-1):
                    word=word.replace("/","")
                curVerse["content"]+=word
            elif(node.name=="seg"):
                tmp="<span class='%s'>%s</span>"%(node["type"],node.string)
                curVerse["content"]+=tmp
            else:
                print(verseId)
                print(node)


        data["verses"].append(curVerse)

       
"""
        for node in verse.find_all():
            #print("name=",node.name)
            if node.name!="w":
                print(node.name)
                print(node)
            if "type" in node.attrs:
                print("type)",node["type"])
"""


with open(inputFile) as fp:
  soup=BeautifulSoup(fp, features='xml')
  for book in soup.find_all('div',type="book"):
    for chapter in book.find_all("chapter"):
       createChapterHtml(chapter)


