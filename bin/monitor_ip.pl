#!/usr/bin/perl -w

# Rights released, ScaleAV, 2019

use strict;
use warnings;

use Time::HiRes;
use Net::Ping;
use Cwd            qw( abs_path );
use File::Basename qw( dirname );

my $datafile        = dirname(dirname(abs_path($0))) . '/config/rooms';
my $ping_timeout    = 0.125;
my $scan_interval   = 5.00;        # Rescan rate in seconds


# Output column titles and associated hostname rules
#   append the suffix to the base hostname to create the associated hardware FQDN
my $machines = [
    # Title        Suffix
    [ 'Host',     '' ],
    [ 'Camera', '-cam' ],
    [ 'Mixer',     '-mixer' ],
];

my $ping = Net::Ping->new();
my $rooms = readFile($datafile);
my $names = [];
foreach my $line (@$rooms) {
    (my $name = $line) =~ s/.*http:\/\///;
    $name =~ s/:8080.*//;
    next if ($name =~ m/^extra/);
    push @$names, $name;
}

main();
exit(0);

sub main {
    clear_screen();
    while (1) {
        home_screen();
        printf("%-25.25s %-8s %-8s %-8s\n", 'Room', map $_->[0], @$machines);
        foreach my $room (sort @$names) {
            printf('%-25.25s', "$room: ");
            foreach my $machine (@$machines) {
                (my $hostname = $room) =~ s/\./$machine->[1]./;
                printf('%s', ($ping->ping($hostname, $ping_timeout))
                    ? green_dot() : red_dot());
            }
            print "\n";
        }
        sleep $scan_interval;
    }
}

sub red_dot {
    return red_fg() . ' R       ' . white_fg();
}

sub green_dot {
    return green_fg() . ' G       ' . white_fg();
}

sub red_fg {
    return "\033[31;1m";
}

sub green_fg {
    return "\033[32;1m";
}

sub white_fg {
    return "\033[37;1m";
}

sub home_screen {
    print "\033[0;0H";
}

sub clear_screen {
    print "\033[2J\033[0;0H";
}

sub readFile {
    my ($file) = @_;

    open FD, "<$file" or die "Error opening file '$file': $!\ n";
    my @output = <FD>;
    close FD;

    chomp @output;
    return \@output;
}

