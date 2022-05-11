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

#Then the module has to be turned into a epub3
#https://ebooks.stackexchange.com/questions/6804/can-kobo-read-hebrew-epubs
#https://www.mobileread.com/forums/showthread.php?p=2973066

#save the epub3 file as hb.kepub
