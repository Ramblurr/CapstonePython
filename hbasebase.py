import settings
import pybase
from pybase.htable import *
from pybase.connection import *
from hbase.ttypes import *
import uuid
import pycassa
from pycassa.system_manager import *
from pycassa.index import *

#yes
class HbaseBase(object):
    def __init__(self):
        self.config = settings.Settings().hbase	
    def test(self):
        sys = pybase.connect([self.config.host])
        print sys.getTableNames()
#no
    def get_record(self, sym):
        it = self.STOCKS.scanner(sym, "price")
        for i in it:
            tcell = i[0].columns
            open = tcell['price:open'].value
            print(open)

#no
    def sym_exists(self, sym):
        sym = sym.upper().strip()
        print "sym exists: " + sym
        key = sym[0]
        results = s

#no
  #  def get_date_range_by_sym(self, sym):
      #  try:
         #   result = self.STOCKS2.get(sym, column_count=14700)
	    #    total_dates = result.keys()
	      #  range = []
	       # range.append(total_dates[0])
	        #range.append(total_dates[len(total_dates)-1])
            #return range
      #  except pycassa.cassandra.ttypes.NotFoundException:
       #     return [
       #     ]
#no
    def get_by_sym_range2(self, sym, start, end):
        print "get_by_sym_range2: start=%s, end=%s" %(start, end)
        scanner = self.STOCKS2.scanner(sym+start, sym+end, "price")
        return scanner
#no
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

#no
    def connect(self, host=None):
        if host is None:
            self.pool = pybase.connect([self.config.host])
            print "connecting to %s" %(self.config.host)
            self.STOCKS = pybase.HTable(self.pool, "Stocks", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')])
            self.DATES = pybase.HTable(self.pool, "Dates", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')])
            self.SYMBOLS = pybase.HTable(self.pool, "Symbols", [ColumnDescriptor(name='symbol:')])

        else:
            self.pool = pybase.connect( [host])
            print "connecting to %s" %(host)
            self.STOCKS = pybase.HTable(self.pool, "Stocks", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')])
            self.DATES = pybase.HTable(self.pool, "Dates", [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')])
            self.SYMBOLS = pybase.HTable(self.pool, "Symbols", [ColumnDescriptor(name='symbol:')])

#yes
    def insert_batch2(self, parser):
        i=0
        last = ''
        for rec in parser:
            symbol = rec['symbol']
            date = rec['date']
            symboldate = symbol+date
            datesymbol = date+symbol
            #del rec['symbol']
            #del rec['date']
            changes = {'price_open':rec['price_open'], 'price_high':rec['price_high'], 'price_low':rec['price_low'], 'price_close':rec['price_close']}
            sym_columnname = 'symbols:' + rec['symbol']
            sym_changes = {sym_columnname:rec['symbol']}
            self.STOCKS.insert(symboldate, changes)
            self.DATES.insert(datesymbol, changes)
#            if last != symbol:
#                self.SYMBOLS.insert(symbol[0], sym_changes)
            last = symbol
      #      if i % 1000 == 0:
       #         print rec
            i += 1
            if i > 1:
                return

#no
    def get_by_symbol(self, symbol):
        scanner = self.STOCKS.scanner(symbol, "price")
        sym_expr = pycassa.create_index_expression("symbol", symbol)
        clause = pycassa.create_index_clause([sym_expr])
        result = self.STOCKS.get_indexed_slices(clause)
        return result
