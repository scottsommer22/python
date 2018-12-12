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

url = 'https://football.fantasysports.yahoo.com/f1/174916/?module=standings&lhst=sched&sctype=team&scmid='

scores = []
for i in range(1,13):
	url = 'https://football.fantasysports.yahoo.com/f1/174916/?module=standings&lhst=sched&sctype=team&scmid='+str(i)
	data = pd.read_html(url)[2]
	data = data['Score'].dropna().map(lambda x: score(x))
	scores.append(data)

df = pd.DataFrame(scores).reset_index().rename(columns = {'index' : 80}).rename(columns = lambda x: "Week "+str(x+1)).rename(columns = {'Week 81' : 'Team Name'})
team_names = pd.read_html(url)[1].drop(0)
team_names = team_names[0].str.split('  ', expand=True).stack()
team_names = pd.DataFrame(team_names).set_index(0).reset_index().rename(columns={0 : 'Team Name',})

df['Team Name'] = team_names
df.rename(columns = lambda x: "Week "+str(x))
print df

#sh = gc.open('2018 Naz 50/50')
#wks = sh[3]
#wks.set_dataframe(df,(17,2))