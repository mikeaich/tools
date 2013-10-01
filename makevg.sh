#!/bin/sh
echo "Backing up stripped files"
mv out/target/product/generic/system/b2g/libmozglue.so out/target/product/generic/system/b2g/libmozglue.so.bak
mv out/target/product/generic/system/b2g/libxul.so out/target/product/generic/system/b2g/libxul.so.bak
# mv out/target/product/generic/system/bin/b2g.sh out/target/product/generic/system/bin/b2g.sh.bak
mv out/target/product/generic/system/lib/libc.so out/target/product/generic/system/lib/libc.so.bak
mv out/target/product/generic/system/lib/libstlport.so out/target/product/generic/system/lib/libstlport.so.bak
mv out/target/product/generic/system/lib/libui.so out/target/product/generic/system/lib/libui.so.bak
echo "Copying symbolified files"
cp objdir-gecko-mc-valgrind/mozglue/build/libmozglue.so out/target/product/generic/system/b2g/libmozglue.so
cp objdir-gecko-mc-valgrind/toolkit/library/libxul.so out/target/product/generic/system/b2g/libxul.so
# cp out/target/product/generic/system/bin/b2g.sh out/target/product/generic/system/bin/b2g.sh
cp out/target/product/generic/symbols/system/lib/libc.so out/target/product/generic/system/lib/libc.so
cp out/target/product/generic/symbols/system/lib/libstlport.so out/target/product/generic/system/lib/libstlport.so
cp out/target/product/generic/symbols/system/lib/libui.so out/target/product/generic/system/lib/libui.so
echo "Rebuilding systemimage"
./bld.sh snod
