#!/usr/bin/perl

use File::Temp qw/ tempfile tempdir unlink0 /;

$/ = "\r\n";
my $out = "";
my @b2gsh = `adb shell cat /system/bin/b2g.sh`;
foreach my $line( @b2gsh ) {
  chomp $line;
  if( $line eq "export NSPR_LOG_MODULES=Camera:4" ) {
    die "Camera debugging already enabled\n";
  } elsif( $line eq "exec /system/b2g/b2g" ) {
    $out .= "export NSPR_LOG_MODULES=Camera:4\n";
  }
  $out .= "$line\n";
}

system "adb remount";
my ( $fh, $name ) = tempfile();
print $fh $out;
system "adb push $name /system/bin/b2g.sh";
system "adb reboot";
unlink0( $fh, $name );
