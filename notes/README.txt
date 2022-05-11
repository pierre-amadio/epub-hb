#clone the morphhb project https://github.com/openscriptures/morphhb

MORPHHBREPO=/home/melmoth/dev/morphhb
rm -rf book
mkdir book
for i in `ls $MORPHHBREPO/wlc`; do
  ./bin/cleanbook.py $MORPHHBREPO/wlc/$i book
done
./bin/createToc.py $MORPHHBREPO/wlc 

cp templates/Foreword.html book/02-Foreword.html

#Get the needed font:
wget https://software.sil.org/downloads/r/ezra/EzraSIL-2.51.zip

#Start sigil
#Add the SILEOT.ttf font in the sigil's font directory
#Add all the html file in the Text directory


