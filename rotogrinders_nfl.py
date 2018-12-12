import pandas as pd
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

urls = ['https://rotogrinders.com/projected-stats/nfl-qb.csv?site=draftkings',
		'https://rotogrinders.com/projected-stats/nfl-rb.csv?site=draftkings',
		'https://rotogrinders.com/projected-stats/nfl-wr.csv?site=draftkings',
		'https://rotogrinders.com/projected-stats/nfl-te.csv?site=draftkings',
		'https://rotogrinders.com/projected-stats/nfl-defense.csv?site=draftkings',
		'https://rotogrinders.com/projected-stats/nfl-kicker.csv?site=draftkings']

array =[]
for i in urls:
	data = pd.read_csv(i,names=["Name","Salary","Team","Position","Opponent","Cell","Floor","Points"])
	array.append(data)

#df = pd.DataFrame(data).sort_values(by='Salary',ascending=False)

df = pd.concat(array).sort_values(by='Salary',ascending=False).set_index('Name').reset_index()

sh = gc.open('Rotogrinders')
wks = sh[0].set_dataframe(df,(1,1))