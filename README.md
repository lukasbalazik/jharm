# JHarm

Json Harmonizator(in short JHarm) is multiple line data convertor. Output is json and it can be send via multiple channels.


## Usage

Every parser have own proccess. You have to start scripts separetly or via init scripts (for example systemd scripts).
```sh
$ ./jh_oneline.py /path/to/parser_config
```

Configuration files are located in /etc/JHarm/.
```
$ cat /etc/JHarm/test_singleline.conf
```
```bash
[connection]
# input informations for listener
input_host=0.0.0.0
input_port=12345

# output for sending
output_host=XXX
output_port=XXX

[detection]
# required keys for creating Json
keys=test

[regex]
# Regexes for converting input to json
test: (?P<test>.*)
```


### Runs
Runs is directory with input classes. Today we have only syslog listener. 

### Parse
Parse is directory with different types of parsing. Actually we have only Regex parsing class.

### Send
Directory with Sending classes, for example zeroMQ, TCP/UDP socket.
