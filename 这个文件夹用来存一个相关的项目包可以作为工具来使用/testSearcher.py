#-*- coding:utf-8 -*-
"""
" ip2region python seacher client module
"
" Autho: koma<komazhang@foxmail.com>
" Date : 2015-11-06



"""
import struct, sys, os, time
from platform import python_version

from ip2Region import Ip2Region

def testSearch():
    """
    " ip2region test function
    """
    argLen     = len(sys.argv)
    version    = python_version()
    algorithms = ["binary", "b-tree", "memory"]

    if argLen < 2:


        return 0

    dbFile = sys.argv[1]

    if (not os.path.isfile(dbFile)) or (not os.path.exists(dbFile)):

        return 0

    if argLen > 2:
        algorithm = sys.argv[2]
    try:
        algorithms.index(algorithm)
    except Exception as e:
        algorithm = "b-tree"








    searcher = Ip2Region(dbFile)

    while True:
        if version[:1] == "2":
            line = raw_input("ip2region>> ")
        else:
            line = input("ip2region>> ")
        line = line.strip()

        if line == "":

            continue

        if line == "quit":

            break

        if not searcher.isip(line):

            continue

        try:
            sTime = time.time()*1000
            if algorithm == "binary":
                data = searcher.binarySearch(line)
            elif algorithm == "memory":
                data = searcher.memorySearch(line)
            else:
                data = searcher.btreeSearch(line)
            eTime = time.time()*1000

        except Exception as e:


    searcher.close()

if __name__ == "__main__":
    testSearch()
