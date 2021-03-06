#!/usr/bin/env python2

import sys
def bytes_per_val(x):
    number = x
    count = 0
    while number > 0:
        number = number / 10
        count = count + 1
    return count

def gen_test(n):
    print "CREATE TABLE t (a BINARY(%d));" % (n)
    for v in [ 0, 1, 2, 4, 8, 16, 32, 64, 126, 127 ]:
        if bytes_per_val(v) > n:
            print "--error ER_DATA_TOO_LONG"
        print "INSERT INTO t VALUES (%d);" % (v)
    for i in range(2,256):
        if i < n:
            print "--replace_regex /MariaDB/XYZ/ /MySQL/XYZ/"
            print "--error ER_UNSUPPORTED_EXTENSION"
        else:
            print "CREATE TABLE ti LIKE t;"
            print "ALTER TABLE ti ENGINE=myisam;"
            print "INSERT INTO ti SELECT * FROM t;"
            print "ALTER TABLE ti CHANGE COLUMN a a BINARY(%d);" % (i)
        print "ALTER TABLE t CHANGE COLUMN a a BINARY(%d);" % (i)
        if i >= n:
            print "let $diff_tables=test.t, test.ti;"
            print "source include/diff_tables.inc;"
            print "DROP TABLE ti;"
    print "DROP TABLE t;"

def main():
    print "source include/have_tokudb.inc;"
    print "# this test is generated by change_bin.py"
    print "# test binary expansion is hot"
    print "--disable_warnings"
    print "DROP TABLE IF EXISTS t,ti;"
    print "--enable_warnings"
    print "SET SESSION DEFAULT_STORAGE_ENGINE=\"TokuDB\";"
    print "SET SESSION TOKUDB_DISABLE_SLOW_ALTER=1;"
    # all n takes too long to run, so here is a subset of tests
    for n in [ 1, 2, 3, 4, 5, 6, 7, 8, 16, 31, 32, 63, 64, 127, 128, 254, 255 ]:
        gen_test(n)
    return 0
sys.exit(main())
