import pandas as pd
import numpy as np
import urllib2
import pygsheets
import time
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

start = datetime.now()

gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

def clean_up(x):
	x = x.replace('Week 14 Matchups Not started yet View Matchup ','x ').replace('Week 14 ','x ').replace('Matchups In progress View Matchup ','').replace(' View Matchup','')
	return " ".join(x.split()[1:-1])

url = 'https://football.fantasysports.yahoo.com/f1/174916/?matchup_week=14'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page,'html.parser')		
data = soup.find('div', attrs={'class': 'Bd No-p Js-submods Tst-matchups-body matchups-body'}).text.strip().encode('ascii','ignore').decode('ascii').rstrip().encode('utf-8')
data = re.sub( '\s+', ' ', data ).strip().replace(' | ','\n').split('\n')

df = pd.DataFrame({'col': data})
df['col'] = df['col'].map(lambda x: clean_up(x))
df = df.drop(df.index[12])
df['Team Name'] = df['col'].map(lambda x:" ".join(x.split(" ")[2:]))
df['Score'] = df['col'].map(lambda x:" ".join(x.split(" ")[0:1]))
df['Proj'] = df['col'].map(lambda x:" ".join(x.split(" ")[1:2]))
df['Week'] = "Week " + url.split("=")[1]
df = pd.DataFrame(df).set_index('Team Name').reset_index()
del df['col']

new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('2018 Nazareth Bowl Playoffs')
wks = sh[2]
wks.set_dataframe(df,(26,1))
wks.update_cell('L1',"Script completed on "+end+", took "+duration+" to run")