#!/usr/bin/perl -w

# Rights released, ScaleAV, 2019
# Monitors ScaleAV hardware and displays status when an item no longer responds
# Plays a sound when an object goes offline for 2 consecutive checks
# Stops the alert and reduces highlighting if offline for over 5 cycles

# FUTURE features
# - Check application level response
#   - http status query and response analysis

# Pragmas
use strict;
use warnings;

# Libraries
use Time::HiRes;
use Net::Ping;
use Cwd            qw( abs_path );
use File::Basename qw( dirname );

# Constants
my $src_dir         = dirname(dirname(abs_path($0)));
my $datafile        = "$src_dir/config/rooms";
my $sound_dir       = "$src_dir/sound";
my $soundfile       = 'danger.mp3';
my $soundfile2      = 'klaxon.mp3';
my $ping_timeout    = 0.125;
my $scan_interval   = 5.00;        # Rescan rate in seconds
my $check_network   = 1;           # Perform a ping test
my $check_app       = 0;           # Perform a protocol status query
my $play_sounds     = 0;
# Define column titles and associated hostname rules
#   append the suffix to the base hostname to create the associated hardware FQDN
my $machines = [
    # Title        Suffix
    [ 'Host',     '' ],
    [ 'Camera', '-cam' ],
    [ 'Mixer',     '-mixer' ],
];


# Derived constants
my $ping = Net::Ping->new();
my $rooms = readFile($datafile);
my $names = [];
my $status = {};
foreach my $line (@$rooms) {
    (my $name = $line) =~ s/.*http:\/\///;
    $name =~ s/:8080.*//;
    next if ($name =~ m/^extra/);
    $status->{$name} = {};
    push @$names, $name;
}

parseArgs(@ARGV);
main();
exit(0);

sub main {
    clear_screen();
    my $sound_toggle = 0;
    while (1) {
        home_screen();
        printf("%-25.25s %-8s %-8s %-8s\n", 'Room', map $_->[0], @$machines);
        my $in_danger = 0;
        foreach my $room (sort @$names) {
            printf('%-25.25s', "$room: ");
            foreach my $machine (@$machines) {
                (my $hostname = $room) =~ s/\./$machine->[1]./;
		if ($check_app) {
                    # For each line determine an application level query and
                    # set of responses.  Use wget or library to send the query
                    # and receive back responses.  If fails check network below
		} elsif ($check_network) {
                    if ($ping->ping($hostname, $ping_timeout)) {
                        $status->{$room}->{$machine} = 0;
                        print green_dot();
                    } else {
                        $status->{$room}->{$machine}++;
                        if ($status->{$room}->{$machine} >= 2 and 
                                $status->{$room}->{$machine} <= 5) {
                            print red_bg(), red_dot(), black_bg();
                            $in_danger = 1;
                        } else {
                            print red_dot();
                        }
                    }
                }
            }
            print "\n";
        }
	play_sound(($sound_toggle++ % 2) ? $soundfile2 : $soundfile)
            if ($play_sounds and $in_danger);
        sleep $scan_interval;
    }
}

sub parseArgs {
    my $USAGE = <<EOF;
Usage:  $0 [--noping|ping] [--noapp|app] [--nosound|sound] [--soundfile=<file>]
    Monitor the hosts listed in the rooms file and indicate which are online
    --ping      Check whether the hardware responds to network requests
    --app       Check whether the application responds to status messages
                    This is more impactful to the end solution than ping
    --sound     Play a sound when a unit stops responding
    --soundfile Specify the file in ../sound to play when something goes offline
EOF
    foreach my $arg (@_) {
        if ($arg eq '--sound') {
            $play_sounds = 1;
            next;
        }

        if ($arg eq '--nosound') {
            $play_sounds = 0;
            next;
        }

        if ($arg eq '--ping') {
            $check_network = 1;
            next;
        }

        if ($arg eq '--noping') {
            $check_network = 0;
            next;
        }

        if ($arg eq '--app') {
            $check_app = 0;
            next;
        }

        if ($arg eq '--noapp') {
            $check_app = 0;
            next;
        }

        if ($arg =~ m/^--soundfile=.+/) {
            ($soundfile = $arg) =~ s/--soundfile=//;
            next;
        }

        if ($arg =~ m/^-/) {
            print STDERR "Unrecognized option: $arg\n";
            exit(1);
        }

        print STDERR "Unrecognized argument: $arg\n";
        exit(2);
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

sub red_bg {
    return "\033[41;1m";
}

sub green_fg {
    return "\033[32;1m";
}

sub white_fg {
    return "\033[37;1m";
}

sub white_bg {
    return "\033[47;1m";
}

sub black_bg {
    return "\033[40;1m";
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

sub play_sound {
    my ($sound) = @_;

    system("cvlc --play-and-exit $sound_dir/$sound > /dev/null 2>/dev/null");
}

