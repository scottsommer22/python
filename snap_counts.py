# ~*~ coding: utf-8 ~*~

import pandas as pd
import urllib2
import pygsheets
import time
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

start = datetime.now()

def position(x):
	return x.split('/')[6].split('.')[0].upper()

#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

urls = ['https://www.fantasypros.com/nfl/reports/snap-counts/lb.php?show=perc','https://www.fantasypros.com/nfl/reports/snap-counts/db.php?show=perc']

all_defense = []
for i in urls:
	data = pd.read_html(i)[0]
	data['Position'] = position(i)
	all_defense.append(data)

data = pd.concat(all_defense)
data = pd.DataFrame(data)
df = pd.DataFrame(data,columns=['Player','Position','Team','TTL','AVG']).set_index('Player').reset_index()
del data['TTL']
del data['AVG']
del data['Team']
del data['Position']
data = data.dropna(axis=1).set_index('Player').reset_index()

df = df.merge(data, on='Player', how='left')
df.rename(columns={
'1' : 'Week 1',
'2' : 'Week 2',
'3' : 'Week 3',
'4' : 'Week 4',
'5' : 'Week 5',
'6' : 'Week 6',
'7' : 'Week 7',
'8' : 'Week 8',
'9' : 'Week 9',
'10' : 'Week 10',
'11' : 'Week 11',
'12' : 'Week 12',
'13' : 'Week 13',
'14' : 'Week 14',
'15' : 'Week 15',
'16' : 'Week 16',
'17' : 'Week 17'
},inplace=True)
#data = pd.DataFrame(data,columns=['Player','Position','Team','Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7','Week 8','Week 9','Week 10','Week 11','Week 12','Week 13','Week 14','Week 15','Week 16','Week 17'])

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('Snap Counts')
wks = sh[0]
wks.set_dataframe(df,(1,1))
#wks.update_cell('BR1',"Script completed on "+end+", took "+duration+" to run")