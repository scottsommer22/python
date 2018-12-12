import pandas as pd
import numpy as np
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

urls = [
'https://football.fantasysports.yahoo.com/f1/174916/1/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/2/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/3/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/4/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/5/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/6/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/7/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/8/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/9/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/10/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/11/team?&week=',
'https://football.fantasysports.yahoo.com/f1/174916/12/team?&week='
]

week_url = 'https://football.fantasysports.yahoo.com/f1/174916'

page = urllib2.urlopen(week_url)
soup = BeautifulSoup(page,'html.parser')		
week = int(soup.find('a', attrs={'class': 'flyout_trigger No-bdr-radius Fz-xs Grid-u No-Hover-Underline'}).text.strip().replace('Week ',''))

array = []
for i in urls:
	for x in range(week-1,week+1):
		df = pd.DataFrame(columns = ["A"],data=['test'])
		url = i+str(x)
		print url
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page,'html.parser')		
		team_name = soup.find('a', attrs={'class': 'Navtarget Py-sm Pstart-lg F-reset Wordwrap-bw No-case'}).text.strip().encode('ascii','ignore').decode('ascii').rstrip().encode('utf-8')
		df['Team Name'] = team_name
		data = soup.find('div', attrs={'class': 'Grid-u Px-med Fz-sm Va-mid'}).text.strip()
		score = float(data.split(': ')[1].split(' pts')[0])
		projected_score = float(data.split('(')[1].split(' ')[0])
		diff = score - projected_score
		df['Week ' +str(x)] = diff
		array.append(df)

data = pd.concat(array,sort=False)
data = data.fillna(0)
del data['A']
data = data.set_index('Team Name').reset_index()
df = pd.DataFrame(data)
df = df.groupby('Team Name').sum().reset_index()
print df
	#score = soup.find('div', attrs={'class': 'Grid-u Px-med Fz-sm Va-mid'}).text.strip().encode('ascii','ignore').decode('ascii').rstrip().encode('utf-8')

sh = gc.open('2018 Naz 50/50')
wks = sh[6]
wks.set_dataframe(df,(17,1))