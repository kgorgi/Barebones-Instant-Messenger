#!/bin/sh

echo Here we GO!!

i=0
max=3
room="Rooom"

xterm -e python3 -m iClient $room Admin &

while [ $i -lt $max ]
do
    echo "output: $i"
    xterm -e python3 -m simulator $room $i &
    true $(( i++ ))
done
