# import logging
# import pandas as pd
# from pathlib import Path
# from sys import argv, stdout

# mylogger = logging.getLogger('foo')
# mylogger.setLevel(logging.INFO)
# mylogger.addHandler(logging.StreamHandler())



# gdf = df.groupby(['state', 'sex', 'name']).sum()
# hdf = gdf.reset_index()
# idf = hdf.groupby(['state', 'sex', 'name'])['count']
# hdf['therank'] = idf.rank(ascending=0, method='min').astype(int)

# hdf = gdf.reset_index().groupby(['state', 'sex', 'name'])['count']
# idf = hdf.rank(ascending=0, method='min').astype(int)


# gdf['alltime_rank_within_sex'] = gdf.groupby(level=['state', 'sex', 'name'])\
#                     ['count'].rank(ascending=0, method='min').astype(int)



# xdf = gdf.reset_index().loc[:, ['state', 'sex', 'name', 'count']]
# df['all_time_rank_within_sex'] = gdf.groupby(['state', 'sex', 'name'])['count']\
#                         .rank(ascending=0, method='min').astype(int)

# gdf['alltime_rank_within_sex'] = gdf['count']\
#         .rank(ascending=0, method='min').astype(int)

# if __name__ == '__main__':
#     src_path = Path(argv[1])
#     if not src_path.is_file():
#         raise IOError("First argument must be a path to a data file. %s is not a file" % src_path)
#     else:
#         mylogger.info("Reading: %s" % src_path)
#         df = pd.read_csv(src_path)
#         df = calculate_and_rank(df)
#         stdout.write(df.to_csv(index=False))
