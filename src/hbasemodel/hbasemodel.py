import settings
import pybase
from pybase.htable import *
from pybase.connection import *
from hbase.ttypes import *
import uuid
import hbase

schema = { 'Stocks':   [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Dates':    [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Symbols':  [ColumnDescriptor(name='symbol:')] }

#yes
class HbaseBase(object):
    def __init__(self):
        self.config = settings.Settings().hbase	
    def test(self):
        sys = pybase.connect([self.config.host])
        print sys.getTableNames()
#yes
    def get_record(self, sym):
        it = self.STOCKS.scanner(sym, "price")
        for i in it:
            tcell = i[0].columns
            open = tcell['price:price_open'].value
            print open

#yes
    def sym_exists(self, sym):
        sym = sym.upper().strip()
        print "sym exists: " + sym
        key = sym[0]
        records = 0
        scanner = self.STOCKS.scanner(sym, "price")
        for i in scanner:
            records = records + 1
        if records > 0:
            return True
        if records == 0:
            return False

#yes
    def get_date_range_by_sym(self, sym):
        scanner = self.STOCKS.scanner(sym, "price")
        dates = []
        for i in scanner:
            date = i[0].row
            date = date.lstrip(sym)
            dates.append(date)
        range = []
        range.append(dates[0])
        range.append(dates[len(dates)-1])
        return range

#yes
    def get_by_sym_range2(self, sym, start, end):
        print "get_by_sym_range2: start=%s, end=%s" %(start, end)
<<<<<<< HEAD
        scanner = self.STOCKS.scanner(sym+start, sym+end, "price")
=======
        scanner = self.STOCKS.scanner(sym+start, sym+end+"A", "price")
>>>>>>> da556aea693dd47f0815b4d373dffe3ec1446bb4
        results = []
        for i in scanner:
            temp = {}
            date = i[0].row
            date = date.lstrip(sym)
            temp['date'] = date
            tcell = i[0].columns 
            print tcell
            temp['price_open'] = tcell['price:price_open'].value
            temp['price_high'] = tcell['price:price_high'].value
            temp['price_low'] = tcell['price:price_low'].value
            temp['price_close'] = tcell['price:price_close'].value
            temp['price_adj_close'] = tecell['price:price_adj_close'].value
            results.append(temp)
        return results

#yes
    def get_symbols_by_partial(self, sym_partial):
        partial = sym_partial.upper()
        key = partial[0]
        last = partial[len(partial)-1]
        before = partial
        after = partial + "ZZZZZ" # Assuming symbol <5 chars long, end is non-inclusive
        scanner = self.SYMBOLS.scanner(key, "symbol")
        for i in scanner:
            results = i[0].columns
            list = []
            for tcell in results.values():
                list.append( tcell.value )
            return list

#yes
    def connect(self, host=None):
        if host is None:
            self.pool = pybase.connect([self.config.host])
            print "connecting to %s" %(self.config.host)
        else:
            self.pool = pybase.connect( [host])
            print "connecting to %s" %(host)

        for name in schema:
            setattr(self, name.upper(), pybase.HTable(self.pool, name, schema[name])) #, createIfNotExist=True, overwrite=False))

#yes
    def insert_batch2(self, parser):
        i=0
        last = ''
        for rec in parser:
            symbol = rec['symbol']
            date = rec['date']
            symboldate = symbol+date
            datesymbol = date+symbol
            
            changes = {}
            fields = ['price_open', 'price_high', 'price_low', 'price_close', 'price_adj_close']
            for field in fields:
                changes['price:' + field] = rec[field]
            
            sym_columnname = 'symbol:symbol_' + rec['symbol']
            sym_changes = {sym_columnname:rec['symbol']}
            self.STOCKS.insert(symboldate, changes)
            self.DATES.insert(datesymbol, changes)
            if last != symbol:
                self.SYMBOLS.insert(symbol[0], sym_changes)
            last = symbol
            if i % 1000 == 0:
                print rec
            i += 1

#yes
    def get_by_symbol(self, symbol):  
        scanner = self.STOCKS.scanner(sym, "price")
        results = []
        for i in scanner:
            temp = {}
            date = i[0].row
            date = date.lstrip(sym)
            temp['date'] = date
            tcell = i[0].columns
            temp['price_open'] = tcell['price:price_open'].value
            temp['price_high'] = tcell['price:price_high'].value
            temp['price_low'] = tcell['price:price_low'].value
            temp['price_close'] = tcell['price:price_close'].value
            temp['price_adj_close'] = tecell['price:price_adj_close'].value
            results.append(temp)
        return results
