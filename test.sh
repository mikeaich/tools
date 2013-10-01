#!/bin/sh
python -c "raise RuntimeError()"
if [ $? == 1 ]; then
  echo Got exception
fi
