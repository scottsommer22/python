import pandas as pd
import urllib2
import pygsheets
import time
import unidecode
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def remove_asterisks(x):
	return x.replace("*","")

start = datetime.now()
#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')


raw_data = []

urls = [
'https://www.hockey-reference.com/leagues/NHL_2008.html',
'https://www.hockey-reference.com/leagues/NHL_2009.html',
'https://www.hockey-reference.com/leagues/NHL_2010.html',
'https://www.hockey-reference.com/leagues/NHL_2011.html',
'https://www.hockey-reference.com/leagues/NHL_2012.html',
'https://www.hockey-reference.com/leagues/NHL_2013.html',
'https://www.hockey-reference.com/leagues/NHL_2014.html',
'https://www.hockey-reference.com/leagues/NHL_2015.html',
'https://www.hockey-reference.com/leagues/NHL_2016.html',
'https://www.hockey-reference.com/leagues/NHL_2017.html',
'https://www.hockey-reference.com/leagues/NHL_2018.html']

for i in urls:
	for x in range(0,2):
		data = pd.read_html(i)[x]
		df = pd.DataFrame(data)
		df['season'] = str(i).split("_")[1].split(".")[0]
		raw_data.append(df)

df = pd.concat(raw_data).dropna().rename(columns={'Unnamed: 0': 'Team Name'})
df['Team Name'] = df['Team Name'].map(lambda x: remove_asterisks(x))
df = pd.DataFrame(df,columns=[
'Team Name',
'season',
'GP',
'W',
'L',
'OL',
'PTS',
'PTS%',
'GF',
'GA',
'SRS',
'SOS',
'RPt%',
'ROW']).sort_values(by=['season','PTS'],ascending=[False,False])

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Standings')
wks = sh[0]
wks.set_dataframe(df,(1,1))
#wks.update_cell('M1',"Script completed on "+end+", took "+duration+" to run")