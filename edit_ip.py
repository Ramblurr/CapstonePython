#!/usr/bin/env python
import socket
import yaml
import os

ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]

config_file = "/etc/cassandra/cassandra.yaml"
stream = file(config_file, 'r')
config = yaml.load(stream)
stream.close()

config['listen_address'] = ip
config['rpc_address'] = "0.0.0.0"
stream = file(config_file, 'w')
yaml.dump(config, stream, default_flow_style=False)

os.system("curl -d \"ip=%s\" 10.242.223.237:8080/seed" % (ip))
