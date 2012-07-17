#!/usr/bin/perl
# written my Mike Habicher, mikeh@mozilla.com, July 2012.
# http://en.wikipedia.org/wiki/Rene_Levesque

use strict;

if( $#ARGV < 0 ) {
  # $ARGV is the array, and $#ARGV gets the highest index in the array
  print "Separates a monolithic diff up into chunks to ease reviewing.\n\n";
  print "usage: rene.pl diff.patch [-t] [rules.txt]\n\n";
  print "       diff.patch  the file containing your monolithic diff\n";
  print "       rules.txt   the file containing the rules used to break up\n";
  print "                     the diff; if not specified, rules.txt is used\n";
  print "       -t          if specified, instead of reading rules.txt,\n";
  print "                     create a rules.txt file containing a default\n";
  print "                     set of rules based on the contents of the diff\n\n";
  exit 0;
}

my $debug = 0;

my $diff_file = $ARGV[0];
my $template_flag = $ARGV[1];
my $rule_file;
my $template_mode = 0;

if( $#ARGV == 0 ) {
  $rule_file = "rules.txt";
} elsif( $#ARGV == 1 ) {
  if( $template_flag ne "-t" ) {
    $rule_file = $ARGV[1];
  } else {
    $rule_file = "rules.txt";
    $template_mode = 1;
  }
} elsif( $#ARGV == 2 && $template_flag eq "-t" ) {
  $rule_file = $ARGV[2];
  $template_mode = 1;
} else {
  die( "Invalid command line arguments\n\n" );
}

open( DIFF, "<", "$diff_file" ) or die( "$diff_file: $!\n" );
my @diff = <DIFF> or die( "$diff_file: $!\n" );
close( DIFF );

my $state = 0;  # initial state
my $filename;
my $lines_before;
my $lines_after;
my $patch;
my %patches = ();

foreach my $line( @diff ) {
  if( $state == 2 ) {
    my $op = substr( $line, 0, 1 );
    if( $op eq "+" ) {
      $lines_before += 1;
      if( $debug ) {
        print "+";
      }
    } elsif( $op eq "-" ) {
      $lines_before -= 1;
      if( $debug ) {
        print "-";
      }
    } elsif( $op ne " " ) {
      if( $lines_before != $lines_after ) {
        die( "\nat end of patch, net $lines_before lines doesn't match goal of $lines_after lines\n" );
      }
      if( $op eq "@" ) {
        $state = 3;
      } else {
        # end of the patch section
        $state = 4;
      }
    } else {
      if( $debug ) {
        print ".";
      }
    }
  }
  if( $state == 1 || $state == 3 ) {
    if( $line =~ m/@@ -(\d+),(\d+) \+(\d+),(\d+) @@/ ) {
      if( $debug ) {
        print "@";
      }
      $lines_before = $2;
      $lines_after = $4;
      $state = 2;
    } elsif( $state == 3 ) {
      die( "Unexpected line format\n\n" );
    } else {
      if( $debug ) {
        print "o";
      }
    }
  }
  if( $state == 4 ) {
    if( $debug ) {
      print "\n";
    }
    $patches{ $filename } = $patch;
    $patch = "";
    $state = 0;
  }
  if( $state == 0 ) {
    if( $line =~ m/diff --git (\S+) (\S+)/ ) {
      $filename = $2;
      if( $debug ) {
        print "found file: $filename\n";
      }
      $state = 1;
    }
  }
  $patch .= $line;
}

if( $template_mode ) {
  open( RULES, ">", "$rule_file" ) or die( "$rule_file: $!\n" );
  print RULES "\@bug:default\n";
  for( keys %patches ) {
    print RULES "=$_:all\n";
  }
  close( RULES );
  print "Generated template file: $rule_file\n\n";
  exit 0;
}

open( RULES, "<", "$rule_file" ) or die( "$rule_file: $!\n" );
my @rulestxt = <RULES> or die( "$rule_file: $1\n" );
close( RULES );

my $bug;
my %rules;

foreach my $rule( @rulestxt ) {
  if( $rule =~ m/\@bug:(\S+)/ ) {
    $bug = $1;
  } elsif( $rule =~ m/=(\S+):(\S+)/ ) {
    push( @{$rules{$2}}, $1 );
  }
}

foreach my $key( keys %rules ) {
  if( $debug ) {
    print "$key:\n";
  }
  my $patch_file = $bug . "_" . $key . ".patch";
  if( $debug ) {
    print "writing: $patch_file\n";
  }
  open( PATCH, ">", "$patch_file" ) or die( "$patch_file: $!\n" );
  foreach( @{$rules{$key}} ) {
    if( $debug ) {
      print "\t$_:\n$patches{$_}\n";
    }
    print PATCH $patches{$_};
  }
  close( PATCH );
}

exit 0;

foreach my $key( keys %rules ) {
  print "$key: @{ $rules{ $key } }\n"
}

exit 0;

for( keys %patches ) {
  print "$_ :\n$patches{ $_ }\n";
}
