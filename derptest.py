import hbasebase
from nasdaq import parser

base = hbasebase.HbaseBase()
base.connect()
data_path = "data/NASDAQ"
p = parser.Parser(data_path)
base.insert_batch2(p)
