import settings
import pycassa
import uuid
from pycassa.system_manager import *
from pycassa.index import *

class CassandraBase(object):
    def __init__(self):
        self.config = settings.Settings().cassandra
    def test(self):
        sys = SystemManager(self.config.host)
        print sys.list_keyspaces()

    def get_by_sym_range(self, sym, start, end):
        sym_expr = pycassa.create_index_expression("symbol", sym)
        start_expr = pycassa.create_index_expression("date", start, GTE)
        end_expr = pycassa.create_index_expression("date", end, LTE)
        clause = pycassa.create_index_clause([sym_expr, start_expr, end_expr])
        result = self.STOCKS.get_indexed_slices(clause)
	return result

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
        self.STOCKS.insert(str(id), record)

    def insert_batch(self, parser):
        b = self.STOCKS.batch(queue_size=1000)
        i = 0
        for rec in parser:
            d = rec['date'].replace("-", "")
            rec['date'] = int(d)
            id = uuid.uuid1()
            b.insert(str(id), rec)
            if i % 1000 == 0:
                print rec
            i += 1

    def get_by_symbol(self, symbol):
        sym_expr = pycassa.create_index_expression("symbol", symbol)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result

    def get_uuid(self, uuid):
        return self.STOCKS.get(uuid)

