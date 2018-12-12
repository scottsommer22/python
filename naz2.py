import pandas as pd
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

#local
gc = pygsheets.authorize(service_file='/Users/scottsommer/libc-roto/creds.json')

#naz_data = []
#for i in range(1,13):
url = 'https://football.fantasysports.yahoo.com/f1/174916/10/team?&week=4'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page,'html.parser')
score = soup.find('div',attrs={'class': 'Ta-end Pend-xl Phone-ta-c Phone-no-p'})

print score
