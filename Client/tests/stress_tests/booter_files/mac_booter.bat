#!/bin/sh

echo Here we GO!!

i=0
max=1
room="Rooom"

# osascript -e 'tell app "Terminal" 
   # do script "cd /Users/Kian/GitHub*Projects/Chat-System-Project/Client; python3 -m tests.stress_tests.iClient '$room' Admin &"
# end tell'


while [ $i -lt $max ]
do
    echo "output: $i"
    osascript -e 'tell app "Terminal"
        do script "cd /Users/Kian/GitHub*Projects/Chat-System-Project/Client
         python3 -m tests.stress_tests.simulator '$room' '$i'"
    end tell'

    osascript -e 'tell application "System Events"
        set visible of process "Terminal" to false
    end tell'
    true $(( i++ ))
done


# For Linux
# xterm -e 