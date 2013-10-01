while [ 1 ]; do
  python runreftestb2g.py --b2gpath ~/dev/mozilla/btg023 --xre-path ~/dev/mozilla/m-c/inbound-src/obj-x86_64-unknown-linux-gnu/dist/bin --remote-webserver 10.0.2.2 --emulator arm --emulator-res 800x1000 --ignore-window-size tests/layout/reftests/reftest.list
  # python runreftestb2g.py --b2gpath ~/dev/mozilla/btg023 --xre-path ~/dev/mozilla/m-c/inbound-src/obj-x86_64-unknown-linux-gnu/dist/bin --remote-webserver 10.0.2.2 --emulator arm --emulator-res 800x1000 --ignore-window-size --total-chunks 10 --this-chunk 1 tests/layout/reftests/reftest.list
  if [ $? -eq 1 ]; then
    echo ========== REFTEST EXCEPTION: BEFORE LOGCAT ==========
    adb logcat -v thread
    echo ========== REFTEST EXCEPTION: AFTER LOGCAT ==========
    exit 1
  fi
done
exit 0
