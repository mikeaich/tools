#!/usr/bin/perl

use File::Temp qw/ tempfile tempdir unlink0 /;

$/ = "\r\n";
my $out = "";
my $found = 0;
my @b2gsh = `adb shell cat /system/bin/b2g.sh`;
foreach my $line( @b2gsh ) {
  chomp $line;
  if( $line eq "export NSPR_LOG_MODULES=Camera:4" ) {
    die "Camera debugging already enabled\n";
  } elsif( $line eq "exec \$COMMAND_PREFIX \"\$B2G_DIR/b2g\"" || $line eq "exec /system/b2g/b2g" ) {
    $out .= "export NSPR_LOG_MODULES=Camera:4\n";
    $found = 1;
  }
  $out .= "$line\n";
}

if( !$found ) {
  die("** Couldn't find command to launch b2g!");
}

system "adb remount";
my ( $fh, $name ) = tempfile();
print $fh $out;
system "adb push $name /system/bin/b2g.sh";
system "adb shell chmod 0755 /system/bin/b2g.sh";
system "adb reboot";
unlink0( $fh, $name );
