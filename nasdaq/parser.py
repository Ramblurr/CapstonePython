"""
Parser for the NASDAQ dataset.

This class acts like a list iterator for the NASDAQ dataset. It transparently 
wraps all the different .csv files in the dataset.

Example usage:
from nasdaq import parser

p = parser.Parser("data/NASDAQ")
    for record in p:
        print record

Example output:
{'price_high': '2.77', 'exchange': 'NASDAQ', 'symbol': 'ABXA', 'price_close': '2.67', 'volum
e': '158500', 'price_open': '2.55', 'date': '2009-12-09', 'price_adj_close': '2.67', 'price_
low': '2.50'}
{'price_high': '2.74', 'exchange': 'NASDAQ', 'symbol': 'ABXA', 'price_close': '2.55', 'volum
e': '131700', 'price_open': '2.71', 'date': '2009-12-08', 'price_adj_close': '2.55', 'price_
low': '2.52'}
...

For performance reasons the len() function is not implemented.

"""
import csv
import collections
from string import ascii_uppercase

class Parser(collections.Iterator):
    def __init__(self,  data_path):
        self.data_path = data_path
        self.letter_iter = iter(ascii_uppercase)
        self._open_next()

    def _open_next(self):
        letter = self.letter_iter.next()
        data  = open(self.data_path+"/NASDAQ_daily_prices_%s.csv" %(letter), "r")
        reader = csv.reader(data)
        self.csv_iter = iter(reader)
        
    def __iter__(self):
        return self

    def _wrap_record(self,  record):
        """
        Turns the record into a dictionary
        """
        keys = ['exchange', 'symbol', 'date', 'price_open', 'price_high', 'price_low', 'price_close', 'volume', 'price_adj_close']
        return dict(zip(keys,  record))

    def next(self):
        try:
            rec = self.csv_iter.next()
            if rec[0] == "exchange": # this skips the header at the beginning of every csv
                rec = self.csv_iter.next()
            return self._wrap_record(rec)
        except StopIteration:
            self._open_next()
            rec = self.csv_iter.next()
            if rec[0] == "exchange":
                rec = self.csv_iter.next()
            return self._wrap_record(rec)
