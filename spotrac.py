import pandas as pd
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

start = datetime.now()

#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

def names_only(x):
    return x.split('(')[0]
def start_year(x):
	return x.split('(')[1].split('-')[0]
def end_year(x):
	return x.split('(')[1].split('-')[1].replace(')','')
url = 'https://www.spotrac.com/nhl/contracts/historical/forward/'
	
	#pull totals by team
contracts = pd.read_html(url)[0]
	
	#pull team name and record

	#convert stats table to DataFrame
df = pd.DataFrame(contracts)

df['Contract Started'] = df['Player'].map(lambda x: start_year(x))
df['Contract Ends'] = df['Player'].map(lambda x: end_year(x))
df['Player'] = df['Player'].map(lambda x: names_only(x))
df['Average'] = df['Average'].replace('[\$,]','',regex=True).astype(float)

df = pd.DataFrame(df,columns=[
	'Player',
	'Contract Started',
	'Contract Ends',
	'Pos',
	'Team',
	'Age',
	'Yrs',
	'Dollars',
	'Average',
	'Free Agent'
	])

df = df.set_index('Player').reset_index().sort_values(by='Average',ascending=False)
fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Data')
wks = sh[3]
wks.set_dataframe(df,(1,1))
wks.update_cell('L1',"Script completed on "+end+", took "+duration+" to run")