#!/bin/bash

# Start up a specified number of test streams on a sequential series of ports

# Usage: $0 [streams] [videofile] [firstport]

# Danger: does a killall vlc so will muck with other running VLC processes

PLAYER='/usr/bin/vlc'
DEBUG=
# DEBUG=echo

COUNT=$1
if [ -z "$COUNT" ] ; then
    COUNT=1
fi

FILE=$2
if [ -z "$FILE" ] ; then
    FILE="$HOME/20150111_150020.mp4"
fi

PORT=$3
if [ -z "$PORT" ] ; then
    PORT=8080
fi

# Shut down any running players giving things time to close out
PS='try'
while [ -n "$PS" ] ; do
    PS=`killall $PLAYER | grep 'no process found' 2>&1`
    sleep 3
done

# Create the requested number of streams
NUM=1
while [ $NUM -le $COUNT ] ; do
    echo "Starting stream $NUM"
    $DEBUG $PLAYER $FILE --play-and-exit --sout \
        "#http{mux=ffmpeg{mux=flv},dst=:$PORT/}" 2>&1 | \
        grep -v 'Running vlc with the default interface' &
    sleep 0.4   # Don't hose the system

    PORT=`expr $PORT + 1`
    NUM=`expr $NUM + 1`
done

