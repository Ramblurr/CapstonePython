#!/usr/bin/env python
"""
 This file is a simple test for the data parser.
 Run it with python test.py
"""
import sys
from nasdaq import parser
from cassandra import cassandramodel
from hbase import hbasemodel
import settings

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

def test_insert2():
    cass = cassandramodel.CassandraBase()
    cass.connect()
    config = settings.Settings()
    data_path = config.data_path
    p = parser.Parser(data_path)
    cass.insert_batch2(p)

def test_hbase():
    hbase = hbasemodel.HbaseBase()
    hbase.connect()
    config = settings.Settings()
    data_path = config.data_path
    p = parser.Parser(data_path)
    hbase.insert_batch2(p)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: test.py cassandra|nasdaq|insert"
        sys.exit(1)
    elif sys.argv[1] == "cassandra":
        test_cassandra()
    elif sys.argv[1] == "hbase":
	    test_hbase()
    elif sys.argv[1] == "nasdaq":
        test_nasdaq()
    elif sys.argv[1] == "insert2":
        test_insert2()
    else:
        print "usage: test.py cassandra|nasdaq|insert2"
