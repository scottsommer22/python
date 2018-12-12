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
def names(x):
	return x.split(" ",1)[1].split(" ",1)[1]
def team_name(x):
	return x.split(" ")[6]
def position(x):
	return x.split("  ")[0][-1:]
def opponent(x):
	return x.split("  ",1)[1]

start = datetime.now()
#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')


raw_data = []

urls = ['https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections']

array = []
for i in urls:
	data = pd.read_html(i)[3]
	data.columns = range(data.shape[1])
	df = pd.DataFrame(data,columns=[0,2])
	df.rename(columns={
	0: 'Name',
	2: 'Salary'
	},inplace=True)
	df['Position'] = df['Name'].map(lambda x: position(x))
	df['Opponent'] = df['Name'].map(lambda x: opponent(x))
	#df['Name'] = df['Name'].map(lambda x: names(x))
	array.append(df)

df = pd.concat(array)

print df

sh = gc.open('Rotogrinders')
wks = sh[1]
wks.set_dataframe(df,(1,1))