"""
 This file is a simple test for the data parser.
 Run it with python test.py
"""
from nasdaq import parser

def test_nasdaq():
    p = parser.Parser("data/NASDAQ")

    for record in p:
        print record

if __name__ == "__main__":
    test_nasdaq()
