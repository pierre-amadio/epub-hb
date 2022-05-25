#clone the morphhb project https://github.com/openscriptures/morphhb

MORPHHBREPO=/home/melmoth/dev/morphhb
rm -rf book
mkdir book
for i in `ls $MORPHHBREPO/wlc`; do
  ./bin/cleanbook.py $MORPHHBREPO/wlc/$i book
done
./bin/createToc.py $MORPHHBREPO/wlc 

cp templates/Foreword.html book/02-Foreword.xhtml

#Get the needed font:
wget https://software.sil.org/downloads/r/ezra/EzraSIL-2.51.zip

#Start sigil
#Create a new v3 ebook
#Add the SILEOT.ttf font in the sigil's font directory
#Add all the html file in the Text directory
#Delete the section1 file

#Add a title to the nav's title node.
#Add the content of the navs's Table of content from the generated nav.xhtml file
#In the content.opf change the page progrression direction  <spine page-progression-direction="rtl">
#add the title in the content.opf


#save the epub3 file as hb.kepub.epub


