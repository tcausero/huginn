import os
import pandas as pd
import click

from client.interest import get_interest
from client.client_obj import client
import client.getting_anomalies as anom

@click.command()
@click.argument('entity')
def client_demo(entity):
	"""Perform a demo of how the client object works"""
	print('Finding interest anomalies for {}:'.format(entity))
	try:
		interest = pd.read_csv(os.path.join('client', 'interest_cache', entity + '.csv'), index_col=0)
		interest.index = interest.index.astype('datetime64[ns]')
	except FileNotFoundError:
		print('Could not find this entity in cache.  Requesting pytrends...')
		interest = get_interest(entity)

	cl = client(entity, interest)
	print('Finding Anomalies:')
	print(cl.get_anomalies(method=anom.version_3, lookback=10))
	print('Fetching relevant NYT links:')
	for key, value in cl.get_nyt_links().items():
		print('{}: {}'.format(key, value))
	# print('Scraping content from links')
	# print('Summarizing content')

if __name__ == "__main__":
	client_demo()

