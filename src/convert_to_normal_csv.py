'''Converts thingsboard csv file dump to 
a more human-readable format.
'''
import pandas as pd
from datetime import datetime
import sys

#IN = 'thingsboard_public_ts_kv_2020_09.csv'
#IN = 'thingsboard_public_ts_kv_2020_08.csv'
IN = sys.argv[1]


# hack to filter-out unwanted keys
ks = pd.read_csv('thingsboard_public_ts_kv_dictionary.csv')
normal_keys = {7,8,9,10,11,13,14,15,16,16,18,19,20}
d = dict()
for k,v in zip(ks['key_id'].values, ks['key'].values):
	d[k] = v

def transform(x):
	return d[x]

def datett(ts):
	return datetime.fromtimestamp(int(ts/1000))

df = pd.read_csv(IN)
df = df[df['key'].isin(normal_keys)]
df['keyv'] = df['key'].apply(transform)
df['datetime'] = df['ts'].apply(datett)
df.dropna(subset=['dbl_v'], inplace=True)

df.to_csv(IN + '.proc.csv', index=False)

