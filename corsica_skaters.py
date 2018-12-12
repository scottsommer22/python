import urllib2
import json
import csv
import pandas as pd
import numpy as np
import pygsheets
from pandas.io.json import json_normalize
from datetime import datetime
from pytz import timezone

gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

def getRows(data):
    # ?? this totally depends on what's in your data
    return []

def string_length(x):
	return len(x) - len(x.replace('.',''))

def clean_up_names(x):
	return ''.join(x.split('.')[:string_length(x)])+' '+''.join(x.split('.')[string_length(x):])

def positions(x):
	return x.replace('L','LW').replace('R','RW')

url1 = ['https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2019&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json']

url = ['https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2019&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2018&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2017&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2016&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2015&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2014&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2013&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2012&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2011&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2010&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2009&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2008&position=any&state=5v5&session=Regular&venue=Any&report=Summary&page[number]=1&page[size]=4000&sort=player&format=json']

array = []
for i in url1:
	data = urllib2.urlopen(i).read()
	data = json.loads(data)
	table = json_normalize(data['players'])
	df = pd.DataFrame(table)
	df = df.fillna('-')
	df["player"] = df["player"].map(lambda x: clean_up_names(x))
	df = df.set_index('player').reset_index()
	array.append(df)

df = pd.concat(array)
df = pd.DataFrame(df,columns=[
'player',
'team',
'season',
'position',
'a',
'cA',
'cF',
'cF%',
'cF%QoC',
'cF%QoT',
'cplusminus',
'g',
'gA',
'gF',
'gF%',
'gP',
'gS',
'gS60',
'gplusminus',
'iCF',
'iCF60',
'iPEND',
'iPENT',
'iPplusminus',
'iSh%',
'ixGF',
'ixGF60',
'p',
'p1',
'p160',
'p60',
'pDO',
'relCF%',
'relGF%',
'relxGF%',
'tOI',
'tOI%',
'tOI%QoC',
'tOI%QoT',
'xGA',
'xGF',
'xGF%',
'xGplusminus',
'zSR'])

df['position'] = df['position'].map(lambda x: positions(x))

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

sh = gc.open('CapSpace Data')
wks = sh[3]
wks.set_dataframe(df,(1,1))
wks.update_cell('AT1',"Script completed on "+end)


#fname = "mydata.csv"
#with open(fname,'wb') as outf:
#    outcsv = csv.writer(outf)
#    outcsv.writerows(getRows(data))
