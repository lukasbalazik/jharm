# JHarm

Json Harmonizator(in short JHarm) is multiple line data convertor. JHarm is part of Analysis Server architecture.

![AnalysisServer](https://github.com/lukasbalazik123/jharm/blob/master/AnalysisServer.png)

Output is json and it can be send via multiple channels.



## Usage

### Plugin starting

Every plugin have multiple configs and every config create new istance of plugin. You have to start plugins separetly or via init scripts (for example systemd scripts).
```sh
$ ./jh_oneline.py /path/to/parser_config
```

### Plugins

| Plugin          | Parser Type | Usage                                              |
| --------------- | ----------- | -------------------------------------------------- |
| jh_oneline      | Regex       | Parse oneline data parser                          |
| jh_multiline    | Regex       | Parse multiple data into single event              |
| jh_waf_jsonload | JsonLoad    | Get event from line (Raw JSON)                     |
| jh_waf_varnish  | Regex       | Get event from data by **start** and **end** regex |
| jh_fail2ban     | Fail2Ban    | Generate event from fail2ban configs               |

### Configs

Configuration files are located in /etc/JHarm/.
```shell
$ cat /etc/JHarm/test_singleline.conf

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
exclude=xxx,xxx,xxx
include=xxx,xxx,xxx

[regex]
# Regexes for converting input to json
regexr: (?P<test>\d*) - (?P<test2>\d*).*
```
Connection section defines data for listening and sending data.
In local syslog-ng you have to put config for sending filtered data to plugins.

```shell
$ cat /etc/syslog-ng/conf.d/03jh_apparmor.conf

destination d_jh_apparmor { tcp("127.0.0.1" port(12301) log_fifo_size(1000)); };
filter f_apparmor { match("apparmor"); };
log {
	source(s_net);
	filter(f_apparmor);
	destination(d_jh_apparmor);
};
```


Detection section defines data that have effect on event

- exclude - exclude data based on **id**
- include - include keep only data with **id** 
- keys - keys are required fields from parsing to send event

Regex section defines regexes for parsing data, posibility of use:

* every group will be loaded into events["<groupname>"] = "value of group" 
* every log is comparing with regex and this comparison is iterated for every regex line in config

### Supported configs

There is already multiple defined configs:

| Name                 | Plugin          | Create event from                   |
| -------------------- | --------------- | ----------------------------------- |
| apparmor.conf        | jh_oneline      | Apparmor DENNIED log                |
| checkpoint_ips.conf  | jh_multiline    | Checkpoint IPS alerts               |
| waf_varnish_vsf.conf | jh_waf_varnish  | Varnish log without line identifier |
| fail2ban.conf        | jh_fail2ban     | Log using fail2ban regexes          |
| esa.conf             | jh_multiline    | ESA logs via MID identifier         |
| ips.conf             | jh_oneline      | Cisco IPS alerts                    |
| opsec.conf           | jh_oneline      | Checkpoint OPSEC events             |
| paloalto.conf        | jh_oneline      | PaloAlto alert                      |
| suricata.conf        | jh_oneline      | Suricata alert                      |
| waf.conf             | jh_waf_jsonload | WAF Varnish json                    |
| windows_sa.conf      | jh_oneline      | Windows security log                |
| wsa.conf             | jh_oneline      | Cisco Web Security Appliance        |


### Parse
Parse is directory with different types of parsing.

* Regex Parsing
* Fail2Ban Parsing
* JsonLoad


### Runs
Runs is directory with input classes. Today we have only syslog listener. 

* Syslog Listener


### Send
Directory with Sending classes.

* ZeroMQ

* TCP/UDP Socket

  

![JHarm](https://github.com/lukasbalazik123/jharm/blob/master/JHarm.png)