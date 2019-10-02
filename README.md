# path2json
Convert whatever is at the end of a path to JSON

The path2json command reads the files in the input directory and puts
their contents into an output file as a JSON dictionary. I made this
command because I wanted an easy way to read /sys/class/net/enp10s0/statistics
and I figured that instead of making another specialized program, I might as
well write something generic that could work in a variety of Linux contexts.

Some things to try:

```
path2json --help
```
Get the real help for this program.

```
path2json -i 2 /sys/class/net/<interface>/statistics /dev/stdout
```

Outputs the statistics for your network interface.

```
path2json -e -i 2 -r /sys/devices/system/edac/mc /dev/stdout
```
Tells you all about the error detection and correction statuses
on your machine.