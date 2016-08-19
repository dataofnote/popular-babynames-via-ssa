from pathlib import Path
from sys import argv, stdout
from csv import DictReader, DictWriter
import re


SRC_TYPES = {
    # nationwide year is encoded in filename, e.g. yob1990.txt
    'nationwide': {'filepattern': 'yob[1-2][0-9][0-9][0-9].txt',  'headers' : ['name', 'sex', 'count']},
    'states':  {'filepattern': '[A-Z][A-Z].TXT', 'headers' : ['state', 'sex', 'year', 'name', 'count']},
}

COMPILED_HEADERS = ['state', 'year', 'name', 'sex', 'count']


def glob_data(src_type, src_dir):
    fpattern = SRC_TYPES[src_type]['filepattern']
    for p in src_dir.glob(fpattern):
        with p.open('r') as rf:
            rows = DictReader(rf, fieldnames=SRC_TYPES[src_type]['headers'])
            if src_type == 'nationwide':
                nyear = re.search(r'\d{4}', p.stem).group()
            for row in rows:
                # nationwide data doesn't have all the columns as states do
                if src_type == 'nationwide':
                    row['state'] = 'US'
                    row['year'] = nyear
                yield row




if __name__ == '__main__':
    """
    argv[1] is nationwide or states
    argv[2] is a directory to glob from
    """
    src_type = argv[1]
    src_dir = Path(argv[2])

    if src_type not in SRC_TYPES.keys():
        raise TypeError("First argument must be: %s" % ', '.join(SRC_TYPES.keys()))
    elif not src_dir.is_dir():
        raise RuntimeError("%s is not a directory" % src_dir)
    csvout = DictWriter(stdout, fieldnames=COMPILED_HEADERS)
    csvout.writeheader()
    for row in glob_data(src_type, src_dir):
        csvout.writerow(row)

