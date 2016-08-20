"""quickie script to filter by years from filename and send to stdout"""

#!/usr/bin/env python
import argparse
from csv import DictReader, DictWriter
from sys import stdout


def filter_by_years(data, start_year, end_year):
    for row in data:
        if row['year'] >= start_year and row['year'] <= end_year:
           yield row



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Filter input file by specified columns")
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--start-year', type=str)
    parser.add_argument('--end-year', type=str)

    args = parser.parse_args()
    start_year = args.start_year or '0000'
    end_year = args.end_year or '9999'
    csvin = DictReader(args.infile)

    csvout = DictWriter(stdout, extrasaction='ignore', fieldnames=csvin.fieldnames)
    # manually write header...because...why not...
    csvout.writeheader()


    for row in filter_by_years(csvin, start_year, end_year):
        csvout.writerow(row)
