import pandas as pd
import urllib2
import pygsheets
import time
import unidecode
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from string import digits

start = datetime.now()
#local
#gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')
#EC2
gc = pygsheets.authorize(service_file='/home/ubuntu/creds.json')

def names(x):
	return x.split(". ",1)[1]


raw_data = []

urls = ['https://www.capfriendly.com/browse/active&display=expiry-year,length&p=']

for i in range(1,32):
	for each_item in urls:
		each_item = str(each_item)+str(i)
		#pull totals by team
		data = pd.read_html(each_item)[0]
		df = pd.DataFrame(data)
		df = df.fillna('-')
		df['PLAYER'] = df['PLAYER'].map(lambda x: names(x))
		#add columns to dataframe
		raw_data.append(df)

capfriendly_data = pd.concat(raw_data)

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('CapFriendly Only')
wks = sh[0]
wks.set_dataframe(capfriendly_data,(1,1))
#wks.update_cell('X1',"Script completed on "+end+", took "+duration+" to run")
wks.update_cell('K1','="+/-"')