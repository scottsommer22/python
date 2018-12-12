import urllib2
import json
import csv
import pandas as pd
import numpy as np
import requests
import pygsheets
from pandas.io.json import json_normalize
from datetime import datetime
from pytz import timezone

gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

def getRows(data):
    # ?? this totally depends on what's in your data
    return []
def clean_up_names(x):
    return x.replace('.', ' ')

def positions(x):
	return x.replace('L','LW').replace('R','RW')

url =[
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2019&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2018&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2017&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2016&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2015&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2014&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2013&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2012&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2011&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2010&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2009&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2008&position=any&state=Any&session=Regular&venue=Any&report=Individual&page[number]=1&page[size]=4000&sort=player&format=json'
]

array = []
for i in url:
	data = requests.get(i).json()
	table = json_normalize(data['players'])
	df = pd.DataFrame(table)
	df = df.fillna('-')
	df["player"] = df["player"].map(lambda x: clean_up_names(x))
	df = df.set_index('player').reset_index()
	array.append(df)

df = pd.concat(array)
df = pd.DataFrame(df,columns = [
'player',
'team',
'season',
'position',
'a',
'a1',
'a160',
'a2',
'a260',
'a60',
'g',
'g60',
'gP',
'gS',
'gS60',
'iBLK',
'iBLK60',
'iCF',
'iCF60',
'iCSh%',
'iFF',
'iFF60',
'iFO%',
'iFOL',
'iFOW',
'iFSh%',
'iGVA',
'iGVA60',
'iHA',
'iHA60',
'iHF',
'iHF60',
'iPEND',
'iPEND60',
'iPENT',
'iPENT60',
'iPplusminus',
'iSF',
'iSF60',
'iSh%',
'iTKA',
'iTKA60',
'ixFSh%',
'ixGF',
'ixGF60',
'p',
'p1',
'p160',
'p60',
'tOI'])

df['position'] = df['position'].map(lambda x: positions(x))

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

sh = gc.open('CapSpace Data')
wks = sh[4]
wks.set_dataframe(df,(1,1))
#wks.update_cell('C18',"Script completed on "+end)


#fname = "mydata.csv"
#with open(fname,'wb') as outf:
#    outcsv = csv.writer(outf)
#    outcsv.writerows(getRows(data))