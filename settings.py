import ConfigParser

class CassandraSettings(object):
    def __init__(self,  host,  keyspace):
        self.host = host
        self.keyspace = keyspace

class Settings(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("settings.cfg")
        
        if self.config.has_section("Cassandra"):
            self.cassandra = CassandraSettings(self.config.get("Cassandra", "host"), self.config.get("Cassandra", "keyspace") )
            
        if self.config.has_section("data"):
            self.data_path = self.config.get("data", "path")
