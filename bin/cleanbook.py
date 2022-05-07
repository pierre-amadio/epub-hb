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
    print(chapterId)
    for verse in chapter.find_all("verse"):
        verseId=verse["osisID"]
        print(verseId)
        for node in verse.find_all():
            #print("name=",node.name)
            if node.name!="w":
                print(node.name)
                print(node)
            if "type" in node.attrs:
                print("type)",node["type"])



with open(inputFile) as fp:
  soup=BeautifulSoup(fp, features='xml')
  for book in soup.find_all('div',type="book"):
    bookId=book["osisID"]
    print(bookId)
    #for chapter in book.find_all("chapter"):
    #   createChapterHtml(chapter)


