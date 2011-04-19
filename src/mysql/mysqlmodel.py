import MySQLdb

class MySqlBase(object):
#    def __init__(self):
	
#    def test(self):

    def sym_exists(self, sym):
	cur = self.dbConn.cursor()
	cur.execute("SELECT Name FROM Symbols WHERE Name=%s", sym)
	results = cur.fetchall()
	return results.len() > 0;
	
#   def get_date_range_by_sym(self, sym):

#    def get_by_sym_range2(self, sym, start, end):

#    def get_symbols_by_partial(self, sym_partial):

    def connect(self, host=None):
	self.dbConn = MySQLdb.connect(host, db="Stocks")
#    def insert(self, record):

#    def insert_batch2(self, parser):

#    def get_by_symbol(self, symbol):

