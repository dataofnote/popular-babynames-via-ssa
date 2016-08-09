"""
Download, save, and unpack the two zip files from ssa.gov.
"""

from pathlib import Path
from shutil import unpack_archive
import requests

FETCHED_DATA_DIR = Path('.', 'datasets', 'babynames', 'fetched')
SRC_URLS = {
    'nationwide': 'https://www.ssa.gov/oact/babynames/names.zip',
    'states': 'https://www.ssa.gov/oact/babynames/state/namesbystate.zip'
}

def main():
    for src_type, src_url in SRC_URLS.items():
        dest_zippath = FETCHED_DATA_DIR.joinpath(src_type + '.zip')
        dest_dir = FETCHED_DATA_DIR.joinpath(src_type)
        dest_dir.mkdir(exist_ok=True, parents=True)

        print("Downloading {0} data from: {1}".format(src_type, src_url))
        response = requests.get(src_url)
        if response.status_code == 200:
            print("Saving to:", dest_zippath)
            dest_zippath.write_bytes(response.content)
            print("Unpacking {0} to {1}:".format(dest_zippath, dest_dir))
            unpack_archive(str(dest_zippath), extract_dir=str(dest_dir))
            filecount = len(list(dest_dir.glob('*')))
            print("Unpacked {0} files".format(filecount))


if __name__ == '__main__':
    main()
