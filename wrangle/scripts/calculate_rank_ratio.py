"""
Calculate each name's rank and per_100k ratio within its group of state+year+sex

Sample output:

| state | year |   sex   | name | count | rank_within_sex | per_100k_within_sex |
|-------|------|---------|------|-------|-----------------|---------------------|
| MS    | 2001 | Beyonce | F    |    22 |             120 |               189.7 |
| NY    | 2001 | Beyonce | F    |    20 |             743 |                20.4 |
| US    | 2001 | Beyonce | F    |   353 |             700 |                19.6 |


How to read this:

In the year 2001, the Social Security Administration registered
22 Mississippi females with the name of "Beyonce". This made it
the 120nd most popular name among females for the state of
Mississippi in the year 2001.

Proportionally speaking, if there were 100,000 females registered
in Mississippi for the year 2001, 189.7 of them would have the
name, "Beyonce".

In contrast, for the entire U.S. in 2001, Beyonce was only the 700th
most popular name among females nationwide, with a ratio of 19.6 per
100,000 females.
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

    returns # type: pandas.DataFrame; a copy of the original dataframe
    """
    # convenience dataframe that has the count column ready to agg by year+state+sex
    df = original_df.copy();
    groupcount_df = original_df.groupby(['year', 'state', 'sex'])['count']

    mylogger.info('Calculating rank values...')
    df['rank_within_sex'] = groupcount_df.rank(ascending=0, method='min').astype(int)

    mylogger.info('Calculating per_100k values')
    # Before calculating per_100k ratio, we need to get the total
    # babies per state,sex,year
    # Create a new dataframe in which `count` is summed by the group
    yrtotal_df = groupcount_df.sum().reset_index()
    # We'll name the aggregate column `yeartotal`
    yrtotal_df = yrtotal_df.rename(columns={'count': 'yeartotal'})
    # Now we join this aggregate dataframe of yearly totals to original dataframe
    # just to make it syntactically easier to calculate the per_100k ratio
    df = pd.merge(df, yrtotal_df, on=['year', 'state', 'sex'])
    # this ratio is of course just count (for a single name) divided by yrtotal
    df['per_100k_within_sex'] = (df['count'] * 100000 / df['yeartotal']).round(1)
    # drop redundant yeartotal column
    df.drop('yeartotal', axis=1, inplace=True)

    return df.sort_values(['year', 'state', 'rank_within_sex', 'sex', 'name'])


if __name__ == '__main__':
    src_path = Path(argv[1])
    if not src_path.is_file():
        raise IOError("First argument must be a path to a data file. %s is not a file" % src_path)
    else:
        mylogger.info("Reading: %s" % src_path)
        df = pd.read_csv(src_path)
        df = calculate_and_rank(df)
        stdout.write(df.to_csv(index=False))

