#!/bin/sh
python -c "raise RuntimeError()"
if [ $? -eq 1 ]; then
  echo Got exception
fi
