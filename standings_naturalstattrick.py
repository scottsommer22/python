import pandas as pd
import urllib2
import pygsheets
import time
import unidecode
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def remove_asterisks(x):
	return x.replace("*","")

start = datetime.now()
#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
#gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

raw_data = []

urls = [
'http://www.naturalstattrick.com/teamtable.php?season=20072008&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2008-10-04&td=2009-04-12',
'http://www.naturalstattrick.com/teamtable.php?season=20082009&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2009-10-01&td=2010-04-11',
'http://www.naturalstattrick.com/teamtable.php?season=20092010&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2010-10-07&td=2011-04-10',
'http://www.naturalstattrick.com/teamtable.php?season=20102011&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2011-10-06&td=2012-04-07',
'http://www.naturalstattrick.com/teamtable.php?season=20112012&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2013-01-19&td=2013-04-28',
'http://www.naturalstattrick.com/teamtable.php?season=20122013&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2013-10-01&td=2014-04-13',
'http://www.naturalstattrick.com/teamtable.php?season=20132014&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&fd=2013-09-14&td=2013-09-29',
'http://www.naturalstattrick.com/teamtable.php?season=20142015&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2015-10-07&td=2016-04-10',
'http://www.naturalstattrick.com/teamtable.php?season=20152016&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2016-10-12&td=2017-04-09',
'http://www.naturalstattrick.com/teamtable.php?season=20162017&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&gpf=82&fd=2017-10-04&td=2018-04-08',
'http://www.naturalstattrick.com/teamtable.php?season=20172018&stype=2&sit=5v5&score=all&rate=n&vs=all&loc=B&fd=2018-09-15&td=2018-10-03',
]

for i in urls:
	data = pd.read_html(i)[0]
	df = pd.DataFrame(data)
	df['Season'] = str(i).split("season=")[1].split("&")[0][-4:]
	raw_data.append(df)

df = pd.concat(raw_data)
df = pd.DataFrame(df, columns=['Team','Season','GP','TOI','W','L','OTL','ROW','CF','CA','CF%','FF','FA','FF%','SF','SA','SF%','GF','GA','GF%','SCF','SCA','SCF%','SCGF','SCGA','SCGF%','SCSH%','SCSV%','HDCF','HDCA','HDCF%','HDGF','HDGA','HDGF%','HDSH%','HDSV%','MDCF','MDCA','MDCF%','MDGF','MDGA','MDGF%','MDSH%','MDSV%','LDCF','LDCA','LDCF%','LDGF','LDGA','LDGF%','LDSH%','LDSV%','SH%','SV%','PDO']).sort_values(by=['Season','W'],ascending=[False,False])

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapSpace Standings')
wks = sh[1]
wks.set_dataframe(df,(1,1))
#wks.update_cell('M1',"Script completed on "+end+", took "+duration+" to run")