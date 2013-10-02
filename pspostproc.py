#!/usr/bin/env python

import re
import sys

def enum(**enums):
    return type('Enum', (), enums)

def main( argv ):
  input = "test.txt"
  State = enum(IDLE=1, GOTTIME=2, GOTHEADER=3)
  state = State.IDLE
  threads = {}
  times = {}
  rt = 0
  if len( argv ) > 0:
    input = argv[0]
  log = open( input )
  for line in log:
    # print line
    line = line.rstrip()
    if state == State.GOTTIME:
      header = re.search( 'PID\s+TID', line )
      if header != None:
        state = State.GOTHEADER
    elif state == State.GOTHEADER:
      # print '==> %s' % line
      ps = re.search( '(\d+)\s+(\d+)\s+\d+\s+(\d+)\%\s+\w\s+\d+K\s+\d+K\s+\w+\s+\w+\s+(\S+)\s*(\S*)', line )
      if ps != None:
        pid = int( ps.group( 1 ) )
        tid = int( ps.group( 2 ) )
        cpu = int( ps.group( 3 ) )
        thread = ps.group( 4 )
        process = ps.group( 5 )
        if cpu > 0:
          if process not in ( 'top', 'sh' ):
            # print 'process: %s(%d), thread: %s(%d), cpu: %d' % ( process, pid, thread, tid, cpu )
            if pid not in threads:
              threads[ pid ] = {}
              threads[ pid ][ 'process' ] = process
              threads[ pid ][ 'cpu' ] = {}
            if tid not in threads[ pid ]:
              threads[ pid ][ tid ] = {}
              threads[ pid ][ tid ][ 'thread' ] = thread
              threads[ pid ][ tid ][ 'cpu' ] = {}
            if pid == tid:
              # Get the latest name for this process and update threads
              threads[ pid ][ 'process' ] = thread
              threads[ pid ][ tid ][ 'thread' ] = thread
            threads[ pid ][ tid ][ 'cpu' ][ rt ] = cpu
            if rt in threads[ pid ][ 'cpu' ]:
              threads[ pid ][ 'cpu' ][ rt ] += cpu
            else:
              threads[ pid ][ 'cpu' ][ rt ] = cpu
            if pid not in times[ rt ]:
              times[ rt ][ pid ] = {}
              times[ rt ][ pid ][ 'cpu' ] = 0
            times[ rt ][ pid ][ tid ] = cpu
            times[ rt ][ pid ][ 'cpu' ] += cpu
      else:
        state = State.IDLE
    if state == State.IDLE:
      uptime = re.search( '(\d+\.\d+) (\d+\.\d+)', line )
      if uptime != None:
        rt = float( uptime.group( 1 ) )
        times[ rt ] = {}
        state = State.GOTTIME
        # print '*** foo: %f' % float( rt )

  times_sorted = sorted( times )
  pids_sorted = sorted( threads )
  
  # Broken down by process -- less detail, more digestible
  if 1:
    # Emit the table header
    print "Timestamp,",
    for pid in pids_sorted:
      print "%s(%d)," % ( threads[ pid ][ 'process' ], pid ),
    print

    # Emit the per-process data
    for ts in times_sorted:
      print "%f," % ts,
      for pid in pids_sorted:
        if ts in threads[ pid ][ 'cpu' ]:
          print "%d," % threads[ pid ][ 'cpu' ][ ts ],
        else:
          print "0,",
      print
    
  # Broken down by thread -- generates a massive, almost unreadable table
  if 0:
    tids_sorted = {}
    for pid in pids_sorted:
      if pid not in tids_sorted:
        tids_sorted[ pid ] = sorted( threads[ pid ] )

    # Emit the table header
    print "Timestamp,",
    for pid in pids_sorted:
      for tid in tids_sorted[ pid ]:
        if type( tid ) is int:
          print "%d:%d," % ( pid, tid ),
    print
  
    # Emit the per-thread data
    for ts in times_sorted:
      print "%f," % ts,
      for pid in pids_sorted:
        for tid in tids_sorted[ pid ]:
          if type( tid ) is int:
            # print "%f, %d, %d," % ( ts, pid, int( tid ) ),
            if ts in threads[ pid ][ tid ][ 'cpu' ]:
              print "%d," % threads[ pid ][ tid ][ 'cpu' ][ ts ],
            else:
              print "0,",
      print
      
if __name__ == "__main__":
  main( sys.argv[1:] )
