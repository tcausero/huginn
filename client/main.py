# !pip install git+https://github.com/GeneralMills/pytrends
# !pip install geopandas
# !pip install colour

from pytrends.request import TrendReq
from matplotlib import pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np

import anomalies as anom
import plotting_anomalies as plt_a
from client_obj import client as client

##################################
# FOR GETTING THE PYTRENDS

def get_interest_over_time(kw_list):
  geo_list = ['US-' + state for state in us_states]
  geo_list.append('US')
  first = True
  for geo in geo_list:  # sometimes takes like 30s using all 50 states
    pytrends.build_payload(kw_list, cat=0, 
                          timeframe='2000-12-14 2017-01-25',
                          geo=geo, gprop='')
    temp = pytrends.interest_over_time().assign(state = geo[-2:])
    if first == False:  # not the first iteration so join the two dfs
      interest = interest.append(temp)
    if first == True:  # on first iteration we initialize interest
      interest = temp
      first = False
  return interest

##################################
# MAIN

if __name__ == "__main__":

	pytrends = TrendReq(hl='en-US', tz=360)

	us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    	         'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
        	     'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
            	 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
            	 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
	
	entity = 'Point72'
	interest = get_interest_over_time([entity]) \
    	          .rename(columns={entity: 'Interest'})
    
	client = client(entity, interest)