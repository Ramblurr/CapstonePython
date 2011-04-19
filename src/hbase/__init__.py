from lib.pybase.htable import *
from lib.pybase.connection import *
from lib.hbase.ttypes import *

schema =
{    
    'Stocks':   [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Dates':    [ColumnDescriptor(name='price:'), ColumnDescriptor(name='volume:')],
    'Symbols':  [ColumnDescriptor(name='symbol:')])
}
