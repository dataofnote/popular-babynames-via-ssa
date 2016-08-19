"""
Calculate each name's rank and per_100k ratio within state+year

Sample output:

| state | year |   sex   | name | count | rank_within_sex | per_100k_within_sex |
|-------|------|---------|------|-------|-----------------|---------------------|
| MS    | 2001 | Beyonce | F    |    22 |             120 |               189.7 |
| NY    | 2001 | Beyonce | F    |    20 |             743 |                20.4 |
| US    | 2001 | Beyonce | F    |   353 |             700 |                19.6 |

"""

import logging
import pandas as pd
from pathlib import Path
from sys import argv, stdout

mylogger = logging.getLogger('foo')
mylogger.setLevel(logging.INFO)
mylogger.addHandler(logging.StreamHandler())


def calculate_and_rank(original_df):
    """
    Reads a CSV data file and calculates columns 'per_100k_within_sex' and 'rank_within_sex'
    args:
        df  # type: pandas.DataFrame

    returns # type: pandas.DataFrame; this is new dataframe
    """

    # first we do a group the names by year and state and sum the counts
    df = original_df.groupby(['year', 'state', 'name']).sum().reset_index()
    # now create an aggregated dataframe to use to do calculations
    groupcount_df = df.groupby(['year', 'state'])['count']

    mylogger.info('Calculating rank values...')
    df['rank'] = groupcount_df.rank(ascending=0, method='min').astype(int)

    mylogger.info('Calculating per_100k values')
    yrtotal_df = groupcount_df.sum().reset_index()
    yrtotal_df = yrtotal_df.rename(columns={'count': 'yeartotal'})
    # Now we join this aggregate dataframe of yearly totals to original dataframe
    # just to make it syntactically easier to calculate the per_100k ratio
    df = pd.merge(df, yrtotal_df, on=['year', 'state'])
    # this ratio is of course just count (for a single name) divided by yrtotal
    df['per_100k'] = (df['count'] * 100000 / df['yeartotal']).round(1)
    # drop redundant yeartotal column
    df.drop('yeartotal', axis=1, inplace=True)

    return df.sort_values(['year', 'state', 'rank', 'name'])


if __name__ == '__main__':
    src_path = Path(argv[1])
    if not src_path.is_file():
        raise IOError("First argument must be a path to a data file. %s is not a file" % src_path)
    else:
        mylogger.info("Reading: %s" % src_path)
        df = pd.read_csv(src_path)
        df = calculate_and_rank(df)
        stdout.write(df.to_csv(index=False))

