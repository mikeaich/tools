#~/bin/sh

adb shell "stop b2g"
adb shell "cd /data/b2g/mozilla/*.default/;echo 'user_pref(\"devtools.debugger.forbid-certified-apps\", false);' >> prefs.js;"
adb shell "start b2g"
