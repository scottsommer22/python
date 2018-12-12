import pandas as pd
import urllib, urllib2
import requests
import cookielib
import pygsheets
import time
from datetime import datetime
from bs4 import BeautifulSoup
from pytz import timezone


start = datetime.now()

gc = pygsheets.authorize(service_file='/Users/scottsommer/scraping/scraper_creds.json')

data = pd.read_csv('/Users/scottsommer/scraping/localmedia.csv')
domains = 'https://www.'+data['domains'].values+'/ads.txt'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

results = []
for x in domains:
	try:
		req = urllib2.Request(x,headers=hdr)
		page = urllib2.urlopen(req,timeout=5).read()
		#soup = BeautifulSoup(page,'html.parser')
		string = str(page).lower()
		if string.find("liveintent.com") != -1:
			results.append('liveintent.com in ads.txt')
			print(x)
		elif string.find("liveintent") != -1:
			results.append('liveintent in ads.txt, needs revision')
		else:
			results.append('No LiveIntent in ads.txt')
			print(x)
	except:
		results.append('No ads.txt')
		print(x)
	time.sleep(.5)

df = pd.DataFrame(results)
df['URL'] = domains
df.rename(columns={0 : 'result'},inplace=True)
df = df.set_index('URL').reset_index()

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

sh = gc.open('Ads.txt')
wks = sh[2]
wks.set_dataframe(df,(1,1))
wks.update_cell('C1',"Script completed on "+end+", took "+duration+" to run")