#!/bin/bash
DIR=`dirname $0`/..
DIR=`cd $DIR; pwd`
{
    cd ${DIR}
    mkdir -p logs
    for stream in `cat $DIR/config/rooms`
    do
        echo "Starting stream: ${stream}"
        python3 -m app.main ${stream} > "logs/${stream//\//_}.log" &
        sleep 1
    done
}
