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
            if(node.name=="rdg" and "type" in node.attrs):
                if(node["type"]=="x-qere"):
                    """
                    Carefull, the x-qere rdg node may contain several w nodes such as in gen 30.11:
                    <w type="x-ketiv" lemma="b/1409" morph="HR/Ncmsa" id="01VG3">ב/גד</w>
                    <note type="variant"><catchWord>ב/גד</catchWord>
                       <rdg type="x-qere">
                         <w lemma="935" morph="HVqrmsa" id="01Q3H">בָּ֣א</w> 
                         <w lemma="1409" n="1" morph="HNcmsa" id="01gKG">גָ֑ד</w>
                       </rdg>
                    </note>
                    """
                    tmpSnt="<span class='x-qere'>["
                    for curw in node.find_all("w"):
                        word=curw.contents[0]
                        if(word.find("/")>-1):
                            word=word.replace("/","")
                        tmpSnt+="%s"%word
                    tmpSnt+="]</span>"
                    curVerse["content"]+=tmpSnt
            elif(node.name=="w"):
                if("type" in node.parent.attrs):
                    if(node.parent["type"]=="x-qere"):
                        continue
                word=node.contents[0]
                if(word.find("/")>-1):
                    word=word.replace("/","")
                curVerse["content"]+="%s "%word
            elif(node.name=="seg"):
                tmp="<span class='%s'>%s</span>"%(node["type"],node.string)
                curVerse["content"]+=tmp
            elif(node.name=="rdg"):
                """Gen.38.24 by exemple:""" 
                continue
            elif(node.name=="note"):
                continue
            elif(node.name=='catchWord'):
                continue
            else:
                """print(verseId)"""
                print("What is this node",verseId,node)


        data["verses"].append(curVerse)

    chapterTemplate = env.get_template("chapter.html")
    chapterOutput = chapterTemplate.render(chapter=data)
    prefix=bookOrder[bookName]
    
    fileOutput="%s/%02d-%s-%03d.html"%(outputDir,prefix,bookId,int(chapterNbr))
    with open(fileOutput,"w") as f:
        f.write(chapterOutput)

       
with open(inputFile) as fp:
  soup=BeautifulSoup(fp, features='xml')
  for book in soup.find_all('div',type="book"):
    for chapter in book.find_all("chapter"):
       createChapterHtml(chapter)
toc=[]
playOrderCnt=1
for ind in range(1,39):
    curBook={}
    curBook["navpointId"]="%03d"%playOrderCnt
    curBook["playOrderId"]="%03d"%playOrderCnt
    curBook["chapters"]=[]
    playOrderCnt+=1
    curBook["name"]=reverseOrder[ind]
    m=re.match("(.*)\/\w+\.xml",inputFile)
    if not m:
        print("Cannot parse inputFile",inputFile)
        sys.exit()

    bookDir=m.group(1)
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
                print(bookHTMLFile)
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


