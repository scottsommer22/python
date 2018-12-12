import urllib2
import json
import csv
import pandas as pd
import numpy as np
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

url = [
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2008&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2009&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2010&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2011&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2012&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2013&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2014&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2015&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2016&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2017&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2018&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json',
'https://api.dailyfaceoff.com/api/player_corsica_stats/goalies.json?api_key=LueJsHh7g7LjSaActxMxZUz1&seasons=2019&state=Any&session=Regular&venue=Any&report=Shots%20Faced&page[number]=1&page[size]=200&sort=player&format=json']

array = []
for i in url:
	data = urllib2.urlopen(i).read()
	data = json.loads(data)
	table = json_normalize(data['players'])
	df = pd.DataFrame(table)
	df = df.fillna('-')
	df["player"] = df["player"].map(lambda x: clean_up_names(x))
	df = df.set_index('player').reset_index()
	array.append(df)

full_set = pd.concat(array)
full_set = pd.DataFrame(full_set,columns=['player','season','team','cA','dSv%','fA','fSv%','gA','gP','gSAA','gSAA30','hDGA','hDSA','hDSv%','lDGA','lDSA','lDSv%','mDGA','mDSA','mDSv%','sA','sv%','tOI','xGA','xSv%']).sort_values(by='season',ascending=False)

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

sh = gc.open('CapSpace Data')
wks = sh[3]
wks.set_dataframe(full_set,(1,1))
#wks.update_cell('C18',"Script completed on "+end)


#fname = "mydata.csv"
#with open(fname,'wb') as outf:
#    outcsv = csv.writer(outf)
#    outcsv.writerows(getRows(data))