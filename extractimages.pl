#!/usr/bin/perl

use strict;
use JSON;
use Encode  qw< encode decode >;

my $reportfile = shift || 'memory-reports';
open( my $IN, '<', $reportfile ) or die( "$reportfile: $!\n" );
my $reportjson = <$IN>;
my $jsonbytes = encode( 'UTF-8', $reportjson );
my $report = JSON->new->utf8->decode_json( $jsonbytes );

print $report;
