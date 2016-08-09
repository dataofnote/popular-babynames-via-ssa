"""
Combine the unzipped nationwide data text files into one file with headers
"""

from pathlib import Path
import csv
import re

DATA_DIR = Path('.', 'datasets', 'babynames')
SRC_DIR = DATA_DIR.joinpath('fetched', 'nationwide')
DEST_PATH = DATA_DIR.joinpath('wrangled', 'nationwide-combined.csv')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
# the original source files do not contain a column for year
# we have to derive that from the filename, e.g. 1995 from yob1995.txt
WRITE_HEADERS = ['year', 'name', 'sex', 'count']

def main():
    total_rowcount = 0
    print("Reading files from:", SRC_DIR)
    print("Writing to:", DEST_PATH)
    destfile = DEST_PATH.open('w')
    destcsv = csv.writer(destfile)
    destcsv.writerow(WRITE_HEADERS);

    for src_path in SRC_DIR.glob('yob*.txt'):
        with src_path.open("r") as srcfile:
            year = re.search('(?<=yob)\d{4}', src_path.stem).group()
            for i, row in enumerate(csv.reader(srcfile)):
                destcsv.writerow([year] + row)
                total_rowcount += 1
            print("\tWrote {0} rows from {1}".format(i+1, src_path))

    print("Wrote {0} rows to {1}".format(total_rowcount, DEST_PATH))
    destfile.close()

if __name__ == "__main__":
    main()
