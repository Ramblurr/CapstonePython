import MySQLdb;

db = MySQLdb.connect(host="localhost", db="Stocks")

c = db.cursor()

c.execute("SELECT * FROM Stocks.Daily WHERE stock_symbol='GOOG'")

keys = ['exchange', 'symbol', 'date', 'price_open', 'price_high', 'price_low', 'price_close', 'volume', 'price_adj_close']
entry = c.fetchone()
dictentry = dict(zip(keys, entry));
print dictentry;
