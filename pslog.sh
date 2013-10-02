#!/bin/sh
echo "Capturing to log.txt . . ."
adb reboot && watch -n 0.1 "adb shell \"cat /proc/uptime && top -n 1 -m 20 -d 0 -t\" >> log.txt"
