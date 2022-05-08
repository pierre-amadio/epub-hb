#1) clone the morphhb project https://github.com/openscriptures/morphhb

MORPHHBREPO=/home/melmoth/dev/morphhb

rm -rf book
mkdir book
for i in `ls $MORPHHBREPO/wlc`; do
  ./bin/cleanbook.py $MORPHHBREPO/wlc/$i book
done



