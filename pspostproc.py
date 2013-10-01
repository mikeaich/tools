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
        if process not in ( 'top', 'sh' ):
          # print 'process: %s(%d), thread: %s(%d), cpu: %d' % ( process, pid, thread, tid, cpu )
          if pid not in threads:
            threads[ pid ] = {}
            threads[ pid ][ 'process' ] = process
          if tid not in threads[ pid ]:
            threads[ pid ][ tid ] = {}
            threads[ pid ][ tid ][ 'thread' ] = thread
            threads[ pid ][ tid ][ 'cpu' ] = {}
          if pid == tid:
            # Get the latest name for this process and update threads
            threads[ pid ][ 'process' ] = thread
            threads[ pid ][ tid ][ 'thread' ] = thread
          threads[ pid ][ tid ][ 'cpu' ][ rt ] = cpu
          if pid not in times[ rt ]:
            times[ rt ][ pid ] = {}
          times[ rt ][ pid ][ tid ] = cpu
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
  
  if 1:
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
      
  if 0:
    for pid in pids_sorted:
      print pid

  if 0:
    for ts in times_sorted:
      # print ts,
      for pid in pids_sorted:
        tids_sorted = sorted( threads[ pid ] )
        for tid in tids_sorted:
          if type( tid ) is int:
            print ts, pid, tid,
      for process in threads_sorted_by_pid:
        print "   ", process[ 0 ]
        print "      ",
        for thread in process[ 1 ]:
          # filter out bookkeeping information
          if type( thread ) is int:
            if ts[ 0 ] in process[ 1 ][ thread ][ 'cpu' ]:
              print process[ 1 ][ thread ][ 'cpu' ][ ts[ 0 ] ],
            else:
              print 0,
   
  if 0:
    for ts, t in times.iteritems():
      # print '%s:' % key
      for id, cpu in t.iteritems():
        # print ' %s %d' % ( id, cpu )
        print 'hello'
        
  if 0:
    for key, t in threads.iteritems():
      if t[ 'process' ] != "":
        print '[%s] %s / %s' % ( key, t[ 'process' ], t[ 'thread' ] )
      else:
        print '[%s] [%s]' % ( key, t[ 'thread' ] )
      for ts, cpu in t[ 'cpu' ].iteritems():
        # print '   %s %s' % ( ts, cpu )
        print '  %s %s%%' % ( ts, cpu )

if __name__ == "__main__":
  main( sys.argv[1:] )
