import settings
import pycassa
from pycassa.system_manager import *

class CassandraBase(object):
    def __init__(self):
        self.config = settings.Settings().cassandra
    def test(self):
        sys = SystemManager(self.config.host)
        print sys.list_keyspaces()

    def create_schema(self):
        sys = SystemManager(self.config.host)
        if not self.keyspace_name in sys.list_keyspaces():
            sys.create_keyspace(self.config.keyspace, replication_factor=1)
        # it probably doesn't make sense to use the UTF8_TYPE here..
        # what should we use instead?
        sys.create_column_family(self.config.keyspace, "Stocks", comparator_type=UTF8_TYPE)

        # create the secondary indexes
        sys.create_index(self.config.keyspace, "Stocks", "symbol", UTF8_TYPE, index_name="symbol_index")

    def connect(self):
        self.pool = pycassa.connect(self.config.keyspace, [self.config.host])
        self.STOCKS = pycassa.ColumnFamily(self.pool, "Stocks")

