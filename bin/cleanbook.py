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
            if(node.name=="w"):
                word=node.contents[0]
                if(word.find("/")>-1):
                    word=word.replace("/","")
                curVerse["content"]+="%s "%word
            elif(node.name=="seg"):
                tmp="<span class='%s'>%s</span>"%(node["type"],node.string)
                curVerse["content"]+=tmp
            elif(node.name=="rdg" and "type" in node.attrs):
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
    fileOutput="html/%03d-%s.html"%(int(chapterNbr),bookId)
    print(fileOutput)
    with open(fileOutput,"w") as f:
        f.write(chapterOutput)

       
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


