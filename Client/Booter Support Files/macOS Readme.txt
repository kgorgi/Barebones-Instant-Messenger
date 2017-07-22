macOS:

Commands:
ulimit -a
launchctl limit maxproc
launchctl limit maxfiles


Kernal
sysctl -w kern.maxprocperuid
sysctl -w kern.maxfiles

plist file location: /Library/LaunchDaemons