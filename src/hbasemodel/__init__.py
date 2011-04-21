from pybase.htable import *
from pybase.connection import *
from hbase.ttypes import *

schema = { 'Stocks':   [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Dates':    [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Symbols':  [ColumnDescriptor(name='symbol:')] }
