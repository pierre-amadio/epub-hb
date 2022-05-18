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
#Add the SILEOT.ttf font in the sigil's font directory
#Add all the html file in the Text directory

#Add a title to the nav's title node.
#Add the content of the navs's Table of content from the generated nav.xhtml file
#In the content.opf change the page progrression direction  <spine page-progression-direction="rtl">



#save the epub3 file as hb.kepub.epub

#####Issues:

nav.xhtml is flat on the kobo:

https://github.com/kobolabs/epub-spec#table-of-contents-toc
https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-nav
https://www.w3.org/publishing/epub3/epub-packages.html#sec-package-nav-def
