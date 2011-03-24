import settings
import pycassa
import uuid
from pycassa.system_manager import *

class CassandraBase(object):
    def __init__(self):
        self.config = settings.Settings().cassandra
    def test(self):
        sys = SystemManager(self.config.host)
        print sys.list_keyspaces()

    def create_schema(self):
        sys = SystemManager(self.config.host)
        if not self.config.keyspace in sys.list_keyspaces():
            sys.create_keyspace(self.config.keyspace, replication_factor=1)
        # it probably doesn't make sense to use the UTF8_TYPE here..
        # what should we use instead?
        #        sys.create_column_family(self.config.keyspace, "Stocks", comparator_type=TIME_UUID_TYPE)

        # create the secondary indexes
        sys.create_index(self.config.keyspace, "Stocks", "symbol", UTF8_TYPE, index_name="symbol_index")

    def connect(self):
        self.pool = pycassa.connect(self.config.keyspace, [self.config.host])
        self.STOCKS = pycassa.ColumnFamily(self.pool, "Stocks")

    def insert(self, record):
        id = uuid.uuid1()
        print id,record
        self.STOCKS.insert(str(id), record)

    def get_symbol(self, symbol):
        sym_expr = pycassa.create_index_expression("symbol", symbol)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result
    def get_uuid(self, uuid):
        print self.STOCKS.get(uuid)

cass = CassandraBase()
cass.connect()
#print cass.get_uuid("7d79917e-5652-11e0-b5e4-0026c649247a")
from nasdaq.parser import Parser
p = Parser("data/NASDAQ")
for record in p:
    cass.insert(p)
