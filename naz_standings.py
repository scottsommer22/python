import pandas as pd
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone


gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

def score(x):
	return x.split(' - ')[0]

url = 'https://football.fantasysports.yahoo.com/f1/174916'

data = pd.read_html(url)[1]
df = pd.DataFrame(data).dropna()
df['Rank'] = df['Rank'].astype(int)
df = df.set_index('Rank').reset_index().sort_values(by='Rank')


print df

sh = gc.open('2018 Naz 50/50')
wks = sh[3]
wks.set_dataframe(df,(1,20))