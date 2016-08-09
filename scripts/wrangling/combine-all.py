"""
Combine the compiled state file and compiled nationwide file into one file with common headers.
"""
from pathlib import Path
from csv import DictReader, DictWriter

DATA_DIR = Path('.', 'datasets', 'babynames', 'wrangled')
DEST_PATH = DATA_DIR.joinpath('all-combined.csv')

SRC_STATES_PATH = DATA_DIR.joinpath('states-combined.csv')
SRC_NATION_PATH = DATA_DIR.joinpath('nationwide-combined.csv')

ALL_HEADERS = ['state', 'year', 'name', 'sex', 'count']

def main():
    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=ALL_HEADERS)
    destcsv.writeheader();

    # start by reading the state file, which
    # requires just a rearrangement of the columns
    print("Reading from:", SRC_STATES_PATH)
    statefile = SRC_STATES_PATH.open('r')
    # this is a very inefficient way to do a rearrangement of
    # columns, but at least it's straightforward...
    for row in DictReader(statefile):
        destcsv.writerow(row)
    statefile.close()

    # now read from the nationwide file, which
    # requires adding a :state key to each dictrow
    # with a value of 'US'
    print("Reading from:", SRC_NATION_PATH)
    nationfile = SRC_NATION_PATH.open('r')
    for row in DictReader(nationfile):
        row['state'] = 'US'
        destcsv.writerow(row)
    nationfile.close()

    # All done
    print("Finished writing to:", DEST_PATH)
    destfile.close()

if __name__ == "__main__":
    main()
