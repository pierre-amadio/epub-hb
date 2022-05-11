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
toc.append({
    "navpointId":"1",
    "playOrderId":"1",
    "name":"Table Of Contents",
    "file":"01-TOC.xhtml"
    })

toc.append({
    "navpointId":"2",
    "playOrderId":"2",
    "name":"Foreword",
    "file":"02-Foreword.xhtml"
    })

playOrderCnt=tocOffset+1
print("Creating TOC")
for ind in range(1,40):
    curBook={}
    curBook["navpointId"]="%s"%playOrderCnt
    curBook["playOrderId"]="%s"%playOrderCnt
    curBook["chapters"]=[]
    playOrderCnt+=1
    curBook["name"]=reverseOrder[ind]
    bookDir=inputFile
    abbr=bookNames[curBook["name"]]
    bookXMLFile="%s/%s.xml"%(bookDir,abbr)
    bookHTMLFile="%02d-%s.xhtml"%(ind+tocOffset,abbr)
    curBook["file"]=bookHTMLFile
    chapterCnt=0
    with open(bookXMLFile) as fp:
        soup=BeautifulSoup(fp,features='xml')
        for book in soup.find_all('div',type="book"):
            for chapter in book.find_all("chapter"):
                curChapter={}
                chapterCnt+=1
                bookHTMLFile="%02d-%s-%03d.xhtml"%(ind+tocOffset,abbr,chapterCnt)
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

htmltocTemplate = env.get_template("TOC.html")
htmltocOutput = htmltocTemplate.render(books=toc)
with open("book/01-TOC.xhtml","w") as f:
    f.write(htmltocOutput)

navTemplate = env.get_template("nav.xhtml")
navOutput = navTemplate.render(books=toc)
with open("nav.xhtml","w") as f:
    f.write(navOutput)


