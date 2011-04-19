import MySQLdb

class MySqlBase(object):
#    def __init__(self):
	
#    def test(self):

    def sym_exists(self, sym):
	cur = self.dbConn.cursor()
	cur.execute("SELECT Name FROM Symbols WHERE Name=%s", sym)
	results = cur.fetchall()
	print "Do we exist? %s " % len(results) > 0 
	return len(results) > 0
	
    def get_date_range_by_sym(self, sym):
        cur = self.dbConn.cursor()
	cur.execute("SELECT min(date), max(date) FROM Daily WHERE stock_symbol=%s", sym);
	result = cur.fetchone()
	ranges = {}
	ranges["min"] = result[0]
	ranges["max"] = result[1]
	
	print ranges
	return ranges

#    def get_by_sym_range2(self, sym, start, end):

    def get_symbols_by_partial(self, sym_partial):
        cur = self.dbConn.cursor()
	begin = sym_partial
	end = sym_partial +'Z'
	cur.execute("SELECT Name FROM Symbols WHERE Name>=%s and Name<=%s", (begin, end))
	query_result = cur.fetchall()

	# We have nested tuples in the results variable
	result = []
	for tup in query_result:
		result.append(tup[0])
	return result

    def connect(self, host=None):
	self.dbConn = MySQLdb.connect(host, db="Stocks")
#    def insert(self, record):

#    def insert_batch2(self, parser):

#    def get_by_symbol(self, symbol):

