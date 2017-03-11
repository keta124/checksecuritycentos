# CheckSecurityCentos
++++++++++++++++

Version 1.1

Check SSH status : user, ip & time login
Check status port change : port open or close
Send log terminal ( OPTION )
+++++++++++++++

 A. Client

- Wget and extract

  $ wget https://github.com/keta124/CheckSecurityCentos/archive/1.4.tar.gz
  
  $ tar xvzf 1.4.tar.gz
  
- Run "python setup.py" ( in folder setup)

  $ cd CheckSecurityCentos-1.4/
  
  $ cd setup
  
  $ python setup.py
  
- Crontab "python monitorATTTMain.py" or call from Appmanager

**** Check server could connect to 192.168.142.101 & iptables open output 192.168.142.101:5044

++++++++++++++++
 
Config send log terminal
 
- Require root access
- Edit /etc/bashrc
 
    $ vi /etc/bashrc
 
Add in last line

    export PROMPT_COMMAND='RETRN_VAL=$?;logger -p local6.info "[$(echo $SSH_CLIENT | cut -d" " -f1)] [$(hostname -I|sed "s/ /||/"g)] # $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//" )"'


- Edit /etc/rsyslog.conf

    $ vi /etc/rsyslog.conf

Add in last line

    local6.info                /var/log/attt_cmdlog.log
- $ chmod 644 /var/log/attt_cmdlog.log

- Restart rsyslog
++++++++++++

 B. Server : Logstash, Elasticsearch, Kibana

++ Config logstash

    filter {
        if [type] == "attt_monitor_cmdlog" {
            grok {
                match => { "message" => "(?<timestamp>%{MONTH}  %{MONTHDAY} %{TIME}) +(?<hostnameserver>%{WORD}) +(?<username>%{WORD}): \[+(?<src_ip>%{IP})\] \[++(?<dest_ip>(?:[0-9\|\.])*[A-Z0-9\|\.])\] \# +(?<terminal>%{GREEDYDATA})"}
            }
        }
        if [type] == "attt_monitor_login" {
            date {
                match => [ "time_stamp", "ISO8601" ]
            }
        }
        if [type] == "attt_monitor_port" {
            date {
                match => [ "time_stamp", "ISO8601" ]
            }
        }
    }
