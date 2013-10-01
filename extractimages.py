#!/usr/bin/env python

import re
import sys
import json
import base64

class ImageRecord:
  def __init__( self, type, data ):
    self.type = type
    self.data = data
    self.count = 1
  def inc( self ):
    self.count += 1

def main( argv ):
  input = "memory-reports"
  if len( argv ) > 0:
    input = argv[0]
  jsondata = open( input )
  data = json.load( jsondata )
  print len( data )
  reports = data["reports"]
  if len( reports ) == 0:
    raise Exception( "No reports section" )
  records = {}
  for r in reports:
    d = r["description"]
    fields = re.search( '(?<=data:image/)([a-z]+)(?:;base64,)([A-Za-z0-9/+=]+)', d )
    if fields != None:
      key = fields.group( 0 )
      if key in records:
        records[ key ].inc()
      else:
        records[ key ] = ImageRecord( fields.group( 1 ), fields.group( 2 ) )
  count = 1
  for key, image in records.items():
    # base64 requires input to be a multiple of 4 bytes
    length = len( image.data )
    extra = length % 4
    if extra:
      data = base64.b64decode( image.data[:-( length % 4 )] )
    else:
      data = base64.b64decode( image.data )
    output = input + "_image-" + "%05d" % count + "." + image.type
    count = count + 1
    print output, length
    f = open( output, 'wb' )
    f.write( data )
    f.close()

if __name__ == "__main__":
  main( sys.argv[1:] )
