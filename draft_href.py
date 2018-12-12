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
'https://www.hockey-reference.com/draft/NHL_2007_entry.html',
'https://www.hockey-reference.com/draft/NHL_2008_entry.html',
'https://www.hockey-reference.com/draft/NHL_2009_entry.html',
'https://www.hockey-reference.com/draft/NHL_2010_entry.html',
'https://www.hockey-reference.com/draft/NHL_2011_entry.html',
'https://www.hockey-reference.com/draft/NHL_2012_entry.html',
'https://www.hockey-reference.com/draft/NHL_2013_entry.html',
'https://www.hockey-reference.com/draft/NHL_2014_entry.html',
'https://www.hockey-reference.com/draft/NHL_2015_entry.html',
'https://www.hockey-reference.com/draft/NHL_2016_entry.html',
'https://www.hockey-reference.com/draft/NHL_2017_entry.html',
'https://www.hockey-reference.com/draft/NHL_2018_entry.html'
]

url = 'https://www.hockey-reference.com/draft/NHL_2007_entry.html'

array = []
for i in urls:
	data = pd.read_html(i)[0]
	data.columns = range(data.shape[1])
	df = pd.DataFrame(data)
	df = df[df[0].notnull()]
	df = df[df[0] != 'Overall'].fillna('-')
	df.set_index(1).reset_index()
	df.rename(columns={
	0: 'Pick',
	1: 'Team',
	2: 'Player Name',
	3: 'Country',
	4: 'Position',
	5: 'Age',
	6: 'To',
	7: 'Amateur Team',
	8: 'GP',
	9: 'G',
	10: 'A',
	11: 'PTS',
	12: 'Plus Minus',
	13: 'PIM',
	14: 'Goalie GP',
	15: 'W',
	16: 'L',
	17: 'T/O',
	18: 'SV%',
	19: 'GAA',
	},inplace=True)
	df['Year'] = str(i).split('_')[1]
	df['Pick'] = df['Pick'].astype(int)
	df = pd.DataFrame(df,columns=['Pick','Year','Team','Player Name','Country','Position','Age','To','Amateur Team','GP','G','A','PTS','Plus Minus','PIM','Goalie GP','W','L','T/O','SV%','GAA'])
	array.append(df)

data = pd.concat(array)
df = pd.DataFrame(data).sort_values(by=['Year','Pick'],ascending=[False,True])

sh = gc.open('CapSpace Draft History')
wks = sh[0]
wks.set_dataframe(df,(1,1))