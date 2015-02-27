#!/usr/bin/python

from itertools import imap
import fileinput
import sys
import re

def analyse(input):
  mem = {}
  module = None
  total_uss = 0
  total_pss = 0

  for line in input:
    match = re.search('[0-9a-f]+-[0-9a-f]+ [rwxsp\-]{4} [0-9a-f]+ [0-9a-f]{2}:[0-9a-f]{2} \d+\s+(.*)', line)
    if match is not None:
      module = match.group(1).strip()
      if module == "":
        module = "[ANONYMOUS]"
      if module not in mem:
        mem[module] = {'pss': 0, 'uss': 0}
      continue
    match = re.search('^Private_Dirty:\s+(\d+)', line)
    if match is not None:
      uss = int(match.group(1).strip())
      mem[module]['uss'] += uss
      total_uss += uss
      continue
    match = re.search('^Pss:\s+(\d+)', line)
    if match is not None:
      pss = int(match.group(1).strip())
      mem[module]['pss'] += pss
      total_pss += pss
      continue
  return mem

def diff(first, second):
  report = {}
  first_keys = sorted(first)
  second_keys = sorted(second)
  for key in first_keys:
    dir = None
    if key in second:
      uss_delta = second[key]['uss'] - first[key]['uss']
      pss_delta = second[key]['pss'] - first[key]['pss']
      second_keys.remove(key)
      dir = 0 # in both
    else:
      uss_delta = -first[key]['uss']
      pss_delta = -first[key]['pss']
      dir = -1 # in first, but not in second
    if uss_delta != 0 or pss_delta != 0:
      report[key] = {'pss': pss_delta, 'uss': uss_delta, 'dir': dir}
  for key in second_keys:
    pss_delta = second[key]['pss']
    uss_delta = second[key]['uss']
    # in second, but not in first
    report[key] = {'pss': pss_delta, 'uss': uss_delta, 'dir': 1}
  return report

def main(files):
  if len(files) > 1:
    file_a = open(files[0], 'r')
    file_b = open(files[1], 'r')
  elif len(files) > 0:
    file_a = open(files[0], 'r')
    file_b = None
  else:
    file_a = sys.stdin
    file_b = None

  mem_a = analyse(file_a)
  file_a.close()
  key_space = max(imap(len, mem_a))
  if file_b is None:
    for key in sorted(mem_a):
      v = mem_a[key]
      if v['pss'] != 0 or v['uss'] != 0:
        print '{key:<{width}} {pss:>7} {uss:>7}'.format(key = key,
                                                                  width = key_space,
                                                                  pss = v['pss'],
                                                                  uss = v['uss'])
  else:
    mem_b = analyse(file_b)
    file_b.close()
    report = diff(mem_a, mem_b)
    key_space = max(imap(len, report))
    for key in sorted(report):
      v = report[key]
      if v['pss'] != 0 or v['uss'] != 0:
        print '{dir} {key:<{width}} {pss:>+7} {uss:>+7}'.format(dir = "-|+"[v['dir'] + 1],
                                                                            key = key,
                                                                            width = key_space,
                                                                            pss = v['pss'],
                                                                            uss = v['uss'])

if __name__ == "__main__":
  main(sys.argv[1:])
