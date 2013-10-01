#!/bin/sh

TS=`date`
QPARENT=`hg id -i -r qparent`
echo "$QPARENT $TS" > .new.good-changesets
if [ -f .good-changesets ]; then
  cat .good-changesets >> .new.good-changesets
  rm .good-changesets
fi
mv .new.good-changesets .good-changesets
