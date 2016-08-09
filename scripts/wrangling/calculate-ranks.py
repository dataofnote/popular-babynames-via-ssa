"""
Calculate each name's rank and per_100k ratio within its group of state+year+sex

i.e.

| state | year | sex | name | rank | per_100k |
|-------|------|-----|------|------|----------|
| DE    | 2012 | M   | Bob  |   25 |    934.2 |

For the state of Delaware in the year 2012, the
name "Bob" was the 25th most popular name among boys,
and if 100,000 baby boys were born in Deleware in 2012,
934.2 of them would be named "Bob"
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path('.', 'datasets', 'babynames', 'wrangled')
SRC_PATH = DATA_DIR.joinpath('all-combined.csv')
DEST_PATH = DATA_DIR.joinpath('all-calculated.csv')

def main():
    print('Opening:', SRC_PATH)
    df = pd.read_csv(SRC_PATH)
    # convenience dataframe that has the count column ready to agg by year+state+sex
    grpcount_df = df.groupby(['year', 'state', 'sex'])['count']

    print('Calculating rank values...')
    df['rank'] = grpcount_df.rank(ascending=0, method='min').astype(int)

    print('Calculating yearly totals...')
    # this is just a sum of the group 'count'
    yrtotals = grpcount_df.sum().reset_index()
    # cleaning up the aggregate dataframe, we'll name the temp column `yrtotal`
    yrtotals = yrtotals.rename(columns={'count': 'yrtotal'})

    # now we join the aggregate dataframe to the original dataframe
    # just for convience of calculating per_100k
    print('Calculating per_100k values')
    df = pd.merge(df, yrtotals, on=['year', 'state', 'sex'])
    df['per_100k'] = (df['count'] * 100000 / df['yrtotal']).round(1)
    # drop redundant yeartotal column
    df.drop('yrtotal', axis=1, inplace=True)

    print('Writing to:', DEST_PATH)
    DEST_PATH.write_text(df.to_csv(index=False))


if __name__ == '__main__':
    main()
