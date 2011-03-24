#!/usr/bin/env python
"""
 This file is a simple test for the data parser.
 Run it with python test.py
"""
import sys
from nasdaq import parser
import settings
import cassandrabase

def test_nasdaq():
    config = settings.Settings()
    data_path = config.data_path
    p = parser.Parser(data_path)

    for record in p:
        print record

def test_cassandra():
    print "Connecting..."
    cass = cassandrabase.CassandraBase()
    cass.test()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: test.py cassandra|nasdaq"
        sys.exit(1)
    elif sys.argv[1] == "cassandra":
        test_cassandra()
    elif sys.argv[1] == "nasdaq":
        test_nasdaq()
    else:
        print "usage: test.py cassandra|nasdaq"