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

    def get_symbols_by_partial(self, sym_partial):
        sym_expr = pycassa.create_index_expression("symbol", sym_partial, GTE)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)


    def connect(self, host=None):
        if not host:
            self.pool = pycassa.connect(self.config.keyspace, [self.config.host])
        else:
            self.pool = pycassa.connect(self.config.keyspace, host)
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

