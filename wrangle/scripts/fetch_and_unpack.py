from pathlib import Path
from shutil import unpack_archive
from sys import argv
import requests

SRC_URLS = {
    'nationwide': 'https://www.ssa.gov/oact/babynames/names.zip',
    'states': 'https://www.ssa.gov/oact/babynames/state/namesbystate.zip'
}


if __name__ == '__main__':
    dtype = argv[1]
    if dtype not in SRC_URLS.keys():
        raise TypeError("First argument must be: %s" % ', '.join(SRC_URLS.keys()))
    dest_dir = Path(argv[2])
    if not dest_dir.is_dir():
        raise RuntimeError("%s is not a directory" % dest_dir)

    src_url = SRC_URLS[dtype]
    print("Downloading:", src_url)
    response = requests.get(src_url)
    if response.status_code != 200:
        raise RuntimeError("Status code %s returned from %s" % (response.status_code, SRC_URL))
    else:
        zippath = dest_dir / (dtype + '.zip')
        print("Saving to:", zippath)
        zippath.write_bytes(response.content)
        print("Unpacking to:", dest_dir)
        unpack_archive(str(zippath), extract_dir=str(dest_dir))
