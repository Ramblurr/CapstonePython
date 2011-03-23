import settings
import pycassa
from pycassa.system_manager import *

class CassandraBase(object):
    def __init__(self):
        cassandra_settings = settings.Settings().cassandra
        self.sys = SystemManager(cassandra_settings.host)
        self.keyspace_name = cassandra_settings.keyspace
    
    def create_schema(self):
        if not self.keyspace_name in self.sys.list_keyspaces():
            self.sys.create_keyspace(self.keyspace_name, replication_factor=1)
            
    def delete_schema(self):
        self.sys.drop_keyspace(self.keyspace_name)
        
    
