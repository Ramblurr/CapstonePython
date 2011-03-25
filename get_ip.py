#!/usr/bin/env python
import socket
import yaml
import os
import urllib2

my_ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
config_file = "/etc/cassandra/cassandra.yaml"
host = "10.242.223.237:8080"

stream = file(config_file, 'r')
config = yaml.load(stream)
stream.close()

seed = urllib2.urlopen("http://%s/seed" %(host)).read().strip()
config['listen_address'] = my_ip
config['seeds'] = [seed]


stream = file(config_file, 'w')
yaml.dump(config, stream, default_flow_style=False)
