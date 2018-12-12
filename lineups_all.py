import pandas as pd
import urllib2
import pygsheets
import time
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

start = datetime.now()

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

urls = [
'https://www.dailyfaceoff.com/teams/anaheim-ducks/line-combinations/',
'https://www.dailyfaceoff.com/teams/arizona-coyotes/line-combinations',
'https://www.dailyfaceoff.com/teams/boston-bruins/line-combinations/',
'https://www.dailyfaceoff.com/teams/buffalo-sabres/line-combinations/',
'https://www.dailyfaceoff.com/teams/calgary-flames/line-combinations/',
'https://www.dailyfaceoff.com/teams/carolina-hurricanes/line-combinations',
'https://www.dailyfaceoff.com/teams/chicago-blackhawks/line-combinations',
'https://www.dailyfaceoff.com/teams/colorado-avalanche/line-combinations',
'https://www.dailyfaceoff.com/teams/columbus-blue-jackets/line-combinations',
'https://www.dailyfaceoff.com/teams/dallas-stars/line-combinations',
'https://www.dailyfaceoff.com/teams/detroit-red-wings/line-combinations',
'https://www.dailyfaceoff.com/teams/edmonton-oilers/line-combinations',
'https://www.dailyfaceoff.com/teams/florida-panthers/line-combinations',
'https://www.dailyfaceoff.com/teams/los-angeles-kings/line-combinations',
'https://www.dailyfaceoff.com/teams/minnesota-wild/line-combinations',
'https://www.dailyfaceoff.com/teams/montreal-canadiens/line-combinations',
'https://www.dailyfaceoff.com/teams/nashville-predators/line-combinations',
'https://www.dailyfaceoff.com/teams/new-jersey-devils/line-combinations',
'https://www.dailyfaceoff.com/teams/new-york-islanders/line-combinations',
'https://www.dailyfaceoff.com/teams/new-york-rangers/line-combinations',
'https://www.dailyfaceoff.com/teams/ottawa-senators/line-combinations',
'https://www.dailyfaceoff.com/teams/philadelphia-flyers/line-combinations',
'https://www.dailyfaceoff.com/teams/pittsburgh-penguins/line-combinations',
'https://www.dailyfaceoff.com/teams/san-jose-sharks/line-combinations',
'https://www.dailyfaceoff.com/teams/st-louis-blues/line-combinations',
'https://www.dailyfaceoff.com/teams/tampa-bay-lightning/line-combinations',
'https://www.dailyfaceoff.com/teams/toronto-maple-leafs/line-combinations',
'https://www.dailyfaceoff.com/teams/vancouver-canucks/line-combinations',
'https://www.dailyfaceoff.com/teams/vegas-golden-knights/line-combinations',
'https://www.dailyfaceoff.com/teams/washington-capitals/line-combinations',
'https://www.dailyfaceoff.com/teams/winnipeg-jets/line-combinations'
]

#put all results from for loops here
full_list = []
for i in urls:
	url = str(i)
	print(i)
	array = []

	forwards = pd.read_html(i)[0]
	defensemen = pd.read_html(i)[1]
	goalies = pd.read_html(i)[6]
	
	df = pd.DataFrame(forwards)
	df_d = pd.DataFrame(defensemen)
	df_g = pd.DataFrame(goalies)
	
	#Forwards
	df = pd.DataFrame(df,columns=['LW','C','RW']).drop([1,3,5,7]).applymap(lambda x: names_only(x)).reset_index()
	df = df.assign(New_ID=[1 + i for i in xrange(len(df))])[['New_ID'] + df.columns.tolist()].astype(str)
	df['LW'] = df['LW'] + ";LW" + df['New_ID']
	df['C'] = df['C'] + ";C" + df['New_ID']
	df['RW'] = df['RW'] + ";RW" + df['New_ID']
	df = pd.DataFrame(df,columns=['LW','C','RW'])
	df = df.values.tolist()
	for i in df:
		array += i
	df = pd.DataFrame(array)
	df['Player Name'], df['LineupCall'] = zip(*df[0].map(lambda x: x.split(';')))
	df['Team'] = url.split('teams/')[1].split('/')[0].replace("-"," ")
	df['Team'] = df['Team'].map(lambda x: abbreviations(x))
	df = pd.DataFrame(df,columns=['Player Name','LineupCall','Team'])
	full_list.append(df)

	#Defensemen
	df = df_d
	df = pd.DataFrame(df,columns=['Defensive Pairings','Defense']).drop([1,3,5]).applymap(lambda x: names_only(x)).reset_index()
	df = df.assign(New_ID=[1 + i for i in xrange(len(df))])[['New_ID'] + df.columns.tolist()].astype(str)
	df['Defensive Pairings'] = df['Defensive Pairings'] + ";LD"+df['New_ID']
	df['Defense'] = df['Defense'] + ";RD" + df['New_ID']
	df = pd.DataFrame(df,columns=['Defensive Pairings','Defense'])
	df = df.values.tolist()
	
	array = []
	for i in df:
		array += i
	df = pd.DataFrame(array)
	df['Player Name'], df['LineupCall'] = zip(*df[0].map(lambda x: x.split(';')))
	df['Team'] = url.split('teams/')[1].split('/')[0].replace("-"," ")
	df['Team'] = df['Team'].map(lambda x: abbreviations(x))
	df = pd.DataFrame(df,columns=['Player Name','LineupCall','Team'])
	full_list.append(df)

	#Goalies
	df = df_g
	df = pd.DataFrame(df).applymap(lambda x: names_only(x))
	df['Goalies'] = df['Goalies'] + ";G1"
	df['Unnamed: 1'] = df['Unnamed: 1'] + ";G2"
	df = pd.DataFrame(df,columns=['Goalies','Unnamed: 1'])
	df = df.values.tolist()
	
	array = []
	for i in df:
		array += i
	df = pd.DataFrame(array)
	df['Player Name'], df['LineupCall'] = zip(*df[0].map(lambda x: x.split(';')))
	df['Team'] = url.split('teams/')[1].split('/')[0].replace("-"," ")
	df['Team'] = df['Team'].map(lambda x: abbreviations(x))
	df = pd.DataFrame(df,columns=['Player Name','LineupCall','Team'])
	full_list.append(df)

full_list = pd.concat(full_list)

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Data')
wks = sh[6]
wks.set_dataframe(full_list,(1,1))
wks.update_cell('L1',"Script completed on "+end+", took "+duration+" to run")