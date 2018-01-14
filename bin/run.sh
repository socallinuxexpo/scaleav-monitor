#!/bin/bash
DIR=`dirname $0`/..
DIR=`cd $DIR; pwd`
{
    cd ${DIR}
    mkdir -p logs
    ITEMS=( `cat $DIR/config/rooms` )
    while  (( ${#ITEMS[@]} >= 2 ))
    do
        echo "Starting stream: ${ITEMS[0]} ${ITEMS[1]}"
        python3 -m app.main ${ITEMS[0]} ${ITEMS[1]} > "logs/${ITEMS[1]//\//_}.log" &
        ITEMS=("${ITEMS[@]:1}")
        ITEMS=("${ITEMS[@]:1}")
        sleep 1
    done
}
