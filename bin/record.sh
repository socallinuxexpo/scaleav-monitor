#!/bin/bash
if (( $# != 2 ))
then
    echo -e "Usage:\n\t$0 <config file> <directory>"
    exit 1
fi
let cnt=0
stream="$2/stream-"
for cnf in $(cat $1)
do
    cvlc --sout "#transcode:file{dst=${stream}${cnt}.ts,no-overwrite}" --sout-keep "${cnf}" &
    let cnt=cnt+1
done
wait
pkill vlc
