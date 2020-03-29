import sys
sys.path.append('client')

from client.interest import get_interest
from client.client_obj import client
import client.getting_anomalies as anom
import pandas as pd
import os

entity = 'Point72'
try:
	interest = pd.read_csv(os.path.join('client', 'interest_cache', entity + '.csv'), index_col=0)
	interest.index = interest.index.astype('datetime64[ns]')
except:
	print('could not find this entity in cache.  requesting pytrends...')
	interest = get_interest(entity)
cl = client(entity, interest)

print(cl.get_anomalies(method=anom.version_3, lookback=10))
