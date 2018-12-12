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

reload(sys)
sys.setdefaultencoding('utf8')

def abbreviations(x):
    return {
'Anaheim Ducks' : 'ANA',
'Arizona Coyotes' : 'ARI',
'Boston Bruins' : 'BOS',
'Buffalo Sabres' : 'BUF',
'Calgary Flames' : 'CGY',
'Carolina Hurricanes' : 'CAR',
'Chicago Blackhawks' : 'CHI',
'Colorado Avalanche' : 'COL',
'Columbus Blue Jackets' : 'CBJ',
'Dallas Stars' : 'DAL',
'Detroit Red Wings' : 'DET',
'Edmonton Oilers' : 'EDM',
'Florida Panthers' : 'FLA',
'Los Angeles Kings' : 'LAK',
'Minnesota Wild' : 'MIN',
'Montreal Canadiens' : 'MTL',
'Nashville Predators' : 'NSH',
'New Jersey Devils' : 'NJD',
'New York Islanders' : 'NYI',
'New York Rangers' : 'NYR',
'Ottawa Senators' : 'OTT',
'Philadelphia Flyers' : 'PHI',
'Pittsburgh Penguins' : 'PIT',
'San Jose Sharks' : 'SJS',
'St Louis Blues' : 'STL',
'Tampa Bay Lightning' : 'TBL',
'Toronto Maple Leafs' : 'TOR',
'Vancouver Canucks' : 'VAN',
'Vegas Golden Knights' : 'VGK',
'Washington Capitals' : 'WSH',
'Winnipeg Jets' : 'WPG'
    }[x]

start = datetime.now()

#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

url = 'http://www.naturalstattrick.com/teamtable.php'

#put all results from for loops here

data = pd.read_html(url)[0]
data['Team'] = data['Team'].map(lambda x: abbreviations(x))
data['Points'] = (2*data['W']) + data['OTL']
data = pd.DataFrame(data,columns=['Team','GP','TOI','W','L','OTL','Points','ROW','CF','CA','CF%','FF','FA','FF%','SF','SA','SF%','GF','GA','GF%','SCF','SCA','SCF%','SCSF','SCSA','SCSF%','SCGF','SCGA','SCGF%','SCSH%','SCSV%','HDCF','HDCA','HDCF%','HDSF','HDSA','HDSF%','HDGF','HDGA','HDGF%','HDSH%','HDSV%','MDCF','MDCA','MDCF%','MDSF','MDSA','MDSF%','MDGF','MDGA','MDGF%','MDSH%','MDSV%','LDCF','LDCA','LDCF%','LDSF','LDSA','LDSF%','LDGF','LDGA','LDGF%','LDSH%','LDSV%','SH%','SV%','PDO']).sort_values(by='Points',ascending=False).set_index('Team').reset_index()

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Data')
wks = sh[6]
wks.set_dataframe(data,(1,1))
#wks.update_cell('L1',"Script completed on "+end+", took "+duration+" to run")