"""
 This file is a simple test for the data parser.
 Run it with python test.py
"""
from nasdaq import parser
import settings

def test_nasdaq():
    config = settings.Settings()
    data_path = config.data_path
    p = parser.Parser(data_path)

    for record in p:
        print record

if __name__ == "__main__":
    test_nasdaq()
