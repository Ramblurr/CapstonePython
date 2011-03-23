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

    def next(self):
        try:
            return self.csv_iter.next()
        except StopIteration:
            self._open_next()
            return self.csv_iter.next()
            
        
