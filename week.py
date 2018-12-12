import pandas as pd
import numpy as np
import urllib2
import pygsheets
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

url = 'https://football.fantasysports.yahoo.com/f1/174916'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page,'html.parser')		
week = int(soup.find('a', attrs={'class': 'flyout_trigger No-bdr-radius Fz-xs Grid-u No-Hover-Underline'}).text.strip().replace('Week ',''))
#week = soup.find('div', attrs={'class': 'Grid-u-1-2'}).text.strip().encode('ascii','ignore').decode('ascii').rstrip().encode('utf-8')

print week