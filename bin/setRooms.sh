#!/bin/bash

# Take a list of rooms from the GoogleDoc source of record and create
# the room configuration file config/rooms 

FILE=~monitor/code/scaleav-monitor/config/rooms
ROOMS='Room 101
Room 103
Room 107
Room 104
Room 106
Room 211
Room 212
Ballroom A
Ballroom B
Ballroom C
Balltoom DE
Ballroom F
Ballroom G
Ballroom H
Extra1
Extra 2
Extra 3'

ROOMCOUNT=`echo "$ROOMS" | wc -l`

mv $FILE $FILE.bk

ROOM=1
while [ $ROOM -le $ROOMCOUNT ] ; do
    echo "$ROOMS" | head -$ROOM | tail -1 | \
        tr '[:upper:]' '[:lower:]' | \
        sed -e 's/ /-/g' \
            -e 's/$/.scaleav.us:8080\/mixed/' \
            -e 's/^/http:\/\//' \
        >> $FILE
    ROOM=`expr $ROOM + 1`
done

