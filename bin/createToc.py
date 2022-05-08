#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup
from globals import *
from jinja2 import Template,FileSystemLoader,Environment

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

inputFile=sys.argv[1]
m=re.search(".*\/(\S+)$",inputFile)
if m:
  shortName=m.group(1)
else:
  shortName=inputFile

toc=[]
playOrderCnt=1
print("Creating TOC")
for ind in range(1,39):
    curBook={}
    curBook["navpointId"]="%03d"%playOrderCnt
    curBook["playOrderId"]="%03d"%playOrderCnt
    curBook["chapters"]=[]
    playOrderCnt+=1
    curBook["name"]=reverseOrder[ind]
    """
    m=re.match("(.*)\/\w+\.xml",inputFile)
    if not m:
        print("Cannot parse inputFile",inputFile)
        sys.exit()
    
    bookDir=m.group(1)
    """
    bookDir=inputFile
    abbr=bookNames[curBook["name"]]
    bookXMLFile="%s/%s.xml"%(bookDir,abbr)
    bookHTMLFile="Text/%02d-%s-%03d.html"%(ind,abbr,1)
    curBook["file"]=bookHTMLFile
    chapterCnt=0
    with open(bookXMLFile) as fp:
        soup=BeautifulSoup(fp,features='xml')
        for book in soup.find_all('div',type="book"):
            for chapter in book.find_all("chapter"):
                curChapter={}
                chapterCnt+=1
                bookHTMLFile="Text/%02d-%s-%03d.html"%(ind,abbr,chapterCnt)
                curChapter["navpointId"]=playOrderCnt
                curChapter["playOrderId"]=playOrderCnt
                playOrderCnt+=1
                curChapter["name"]=chapterCnt
                curChapter["file"]=bookHTMLFile
                curBook["chapters"].append(curChapter)
    toc.append(curBook)


tocTemplate = env.get_template("toc.ncx")
tocOutput = tocTemplate.render(books=toc)
with open("toc.ncx","w") as f:
    f.write(tocOutput)


