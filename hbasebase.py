import settings
import pybase
import uuid
from pycassa.system_manager import *
from pycassa.index import *

class HbaseBase(object):
    def __init__(self):
        self.config = settings.Settings().hbase	
    def test(self):
        sys = pybase.connect([self.config.host])
        print sys.getTableNames()

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
	    range = []
	    range.append(total_dates[0])
	    range.append(total_dates[len(total_dates)-1])
            return range
        except pycassa.cassandra.ttypes.NotFoundException:
            return []

    def get_by_sym_range(self, sym, start, end):
        sym_expr = pycassa.create_index_expression("symbol", sym)
        start_expr = pycassa.create_index_expression("date", start, GTE)
        end_expr = pycassa.create_index_expression("date", end, LTE)
        clause = pycassa.create_index_clause([sym_expr, start_expr, end_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result

    def get_by_sym_range2(self, sym, start, end):
        print "get_by_sym_range2: start=%s, end=%s" %(start, end)
        scanner = self.STOCKS2.scanner(sym+start, sym+end, "price")
        return scanner

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
            self.pool = pybase.connect([self.config.host])
            print "connecting to %s" %(self.config.host)
        else:
            self.pool = pybase.connect( [host])
            print "connecting to %s" %(host)
        self.STOCKS2 = pybase.HTable(self.pool, "Stocks2", [ColumnDescriptor(name='price:'),ColumnDescriptor(name='volume:'),])
        self.SYMBOLS = pybase.HTable(self.pool, "StockSymbols", [ColumnDescriptor(name='symbol:'),])

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

    def insert_batch2(self, parser):
        a  = HTable(client, "Stocks2", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')], createIfNotExist=True, overwrite=False)
        b  = HTable(client, "Symbols", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')], createIfNotExist=True, overwrite=False)
        i =0

        for rec in parser:
            symbol = rec['symbol']
            date = rec['date']
	    symboldate = symbol+date
	    datesymbol = date+symbol
            #del rec['symbol']
            #del rec['date']
	    changes = {"price:open":rec['price_open'], "price:high":rec['price_high'], "price:low":rec['price_low'], "price:close":rec['price_close']}
            a.insert(symboldate, changes)
            b.insert(datesymbol, changes)
            if i % 1000 == 0:
                print rec

    def get_by_symbol(self, symbol):
        sym_expr = pycassa.create_index_expression("symbol", symbol)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result

    def get_uuid(self, uuid):
        return self.STOCKS.get(uuid)

