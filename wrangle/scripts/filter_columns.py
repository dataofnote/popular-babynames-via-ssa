"""quickie script to filter by years from filename and send to stdout"""

#!/usr/bin/env python
import argparse
from csv import DictReader, DictWriter
from sys import stdout


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Filter input file by specified columns")
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--start-year', type=str)
    parser.add_argument('--end-year', type=str)
    parser.add_argument('--states', type=str, help="Comma-delimited list of states to filter by, e.g. 'US,AK'")
    parser.add_argument('--rank', type=int, help="Include names with rank less than or equal to")

    args = parser.parse_args()
    start_year = args.start_year or '0000'
    end_year = args.end_year or '9999'
    name_rank = args.rank
    states = (args.states).split(',') if args.states else []

    csvin = DictReader(args.infile)

    csvout = DictWriter(stdout, extrasaction='ignore', fieldnames=csvin.fieldnames)
    # manually write header...because...why not...
    csvout.writeheader()

    for row in csvin:
        if row['year'] >= start_year and row['year'] <= end_year:
            if not states or row['state'] in states:
                if not name_rank or int(row['rank_within_sex']) <= name_rank:
                    csvout.writerow(row)
        else:
            pass

