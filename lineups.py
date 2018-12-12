import pandas as pd
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def names_only(x):
    return x.split('Rating:')[0]

def team_names(x):
	x.split('teams/')[1].split('/')[0].replace("-"," ")

def abbreviations(x):
    return {
    'anaheim ducks' : 'ANA',
	'arizona coyotes' : 'ARI',
	'boston bruins' : 'BOS',
	'buffalo sabres' : 'BUF',
	'calgary flames' : 'CGY',
	'carolina hurricanes' : 'CAR',
	'chicago blackhawks' : 'CHI',
	'colorado avalanche' : 'COL',
	'columbus blue jackets' : 'CBJ',
	'dallas stars' : 'DAL',
	'detroit red wings' : 'DET',
	'edmonton oilers' : 'EDM',
	'florida panthers' : 'FLA',
	'los angeles kings' : 'LAK',
	'minnesota wild' : 'MIN',
	'montreal canadiens' : 'MTL',
	'nashville predators' : 'NSH',
	'new jersey devils' : 'NJD',
	'new york islanders' : 'NYI',
	'new york rangers' : 'NYR',
	'ottawa senators' : 'OTT',
	'philadelphia flyers' : 'PHI',
	'pittsburgh penguins' : 'PIT',
	'san jose sharks' : 'SJS',
	'st louis blues' : 'STL',
	'tampa bay lightning' : 'TBL',
	'toronto maple leafs' : 'TOR',
	'vancouver canucks' : 'VAN',
	'vegas golden knights' : 'VGK',
	'washington capitals' : 'WSH',
	'winnipeg jets' : 'WPG'
    }[x]

start = datetime.now()

#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

url = 'https://www.dailyfaceoff.com/teams/vegas-golden-knights/line-combinations'	
	#pull totals by team
forwards = pd.read_html(url)[0]
defensemen = pd.read_html(url)[1]
goalies = pd.read_html(url)[2]
	
	#pull team name and record

	#convert stats table to DataFrame
total = []
df = pd.DataFrame(forwards)
df = pd.DataFrame(df,columns=['LW','C','RW']).drop([1,3,5,7]).applymap(lambda x: names_only(x)).reset_index()
df = df.assign(New_ID=[1 + i for i in xrange(len(df))])[['New_ID'] + df.columns.tolist()].astype(str)
df['LW'] = df['LW'] + ";LW"+df['New_ID']
df['C'] = df['C'] + ";C"+df['New_ID']
df['RW'] = df['RW'] + ";RW"+df['New_ID']
df = pd.DataFrame(df,columns=['LW','C','RW'])
df = df.values.tolist()
for i in df:
	total += i
df = pd.DataFrame(total)
df['Player Name'], df['LineupCall'] = zip(*df[0].map(lambda x: x.split(';')))
df['Team'] = url.split('teams/')[1].split('/')[0].replace("-"," ")
df['Team'] = df['Team'].map(lambda x: abbreviations(x))
df = pd.DataFrame(df,columns=['Player Name','LineupCall','Team'])



fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Data')
wks = sh[4]
wks.set_dataframe(df,(1,10))
#wks.update_cell('A1',df)
#wks.update_cell('L1',"Script completed on "+end+", took "+duration+" to run")