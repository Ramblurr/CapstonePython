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

    def sym_exists(self, sym):
	try:
            sym = sym.upper().strip()
            print "sym exists: " + sym
            key = sym[0]
	    results = self.SYMBOLS.get(key, columns=[sym])
	    return True
	except pycassa.cassandra.ttypes.NotFoundException:
	    return False

    def get_date_range_by_sym(self, sym):
        try:
            result = self.STOCKS2.get(sym, column_count=14700)
	    total_dates = result.keys()
	    range = {}
	    range['min'] = total_dates[0]
	    range['max'] = total_dates[len(total_dates)-1]
            return range
        except pycassa.cassandra.ttypes.NotFoundException:
            return []

    def get_by_sym_range2(self, sym, start, end):
        print "get_by_sym_range2: start=%s, end=%s" %(start, end)
        try:
            result = self.STOCKS2.get(sym, column_count=14700, column_start=start, column_finish=end)
            return result.items()
        except pycassa.cassandra.ttypes.NotFoundException:
            return []

    def get_symbols_by_partial(self, sym_partial):
        partial = sym_partial.upper()
        key = partial[0]
        last = partial[len(partial)-1]
        before = partial
        after = partial + "Z"
        try:
            result = self.SYMBOLS.get(key, column_start=before, column_finish=after)
            return result.keys()
        except pycassa.cassandra.ttypes.NotFoundException:
            return []

    def connect(self, host=None):
        if host is None:
            self.pool = pycassa.connect(self.config.keyspace, [self.config.host])
            print "connecting to %s" %(self.config.host)
        else:
            self.pool = pycassa.connect(self.config.keyspace, [host])
            print "connecting to %s" %(host)
        self.STOCKS2 = pycassa.ColumnFamily(self.pool, "Stocks2")
        self.SYMBOLS = pycassa.ColumnFamily(self.pool, "StockSymbols")

    def insert(self, record):
        id = uuid.uuid1()
        self.STOCKS.insert(str(id), record)

    def insert_batch2(self, parser):
        b = self.STOCKS2.batch(queue_size=1000)
        i = 0
        last = ''
        for rec in parser:
            symbol = rec['symbol']
            date = rec['date']
            b.insert(symbol, {date: rec})
            b.insert(date, {symbol: rec})
            if last != symbol:
                self.SYMBOLS.insert(symbol[0], {symbol:''})
            last = symbol
            if i % 1000 == 0:
                print rec
            i += 1

    def get_by_symbol(self, symbol):
        sym_expr = pycassa.create_index_expression("symbol", symbol)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result
