#!/usr/bin/python3

import sys,re
import pandas as pd
import xlrd

def read_xls(infile):
    data = xlrd.open_workbook(infile)
    table = data.sheets()[0]
    nrows = table.rows
    for i in range(nrows):
        row = table.row(i)
        print(row)

if __name__ == "__main":
    infile = sys.argv[1]
    read_xls(infile)