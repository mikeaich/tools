#!/bin/sh
rm log.txt
# watch -n 0.1 "adb shell \"cat /proc/uptime && top -n 1 -m 20 -d 0 -t\" >> log.txt"
adb wait-for-device
echo "Capturing to log.txt . . ."
adb shell "top -m 10 -d 100 -t -u" >> log.txt
