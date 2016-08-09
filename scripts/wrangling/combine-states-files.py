"""
Combine the unzipped state data text files into one file with headers
"""

from pathlib import Path
import csv

DATA_DIR = Path('.', 'datasets', 'babynames')
SRC_DIR = DATA_DIR.joinpath('fetched', 'states')
DEST_PATH = DATA_DIR.joinpath('wrangled', 'states-combined.csv')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

HEADERS = ['state', 'sex', 'year', 'name', 'count']


def main():
    total_rowcount = 0
    print("Reading files from:", SRC_DIR)
    print("Writing to:", DEST_PATH)
    destfile = DEST_PATH.open('w')
    destcsv = csv.writer(destfile)
    destcsv.writerow(HEADERS);

    for src_path in SRC_DIR.glob('*.TXT'):
        with src_path.open("r") as srcfile:
            for i, row in enumerate(csv.reader(srcfile)):
                destcsv.writerow(row)
                total_rowcount += 1
            print("\tWrote {0} rows from {1}".format(i+1, src_path))

    print("Wrote {0} rows to {1}".format(total_rowcount, DEST_PATH))
    destfile.close()


if __name__ == "__main__":
    main()
