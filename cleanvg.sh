#!/bin/sh
echo "Deleting old versions of symbolified files"
rm objdir-gecko-mc-valgrind/mozglue/build/libmozglue.so
rm objdir-gecko-mc-valgrind/toolkit/library/libxul.so
rm out/target/product/generic/symbols/system/lib/libc.so
rm out/target/product/generic/symbols/system/lib/libstlport.so
rm out/target/product/generic/symbols/system/lib/libui.so
