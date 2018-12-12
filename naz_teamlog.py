import pandas as pd
import urllib2
import pygsheets
import time
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
for i in range(1,13):
	url = 'https://football.fantasysports.yahoo.com/f1/174916/'+str(i)+'/teamlog'
	data = pd.read_html(url)[1]
	data.columns = range(data.shape[1])
	df = data.loc[data[1] == 'Totals']
	df = pd.DataFrame(df)
	df = pd.DataFrame(df).set_index(2).reset_index()
	df.drop(df.columns[[1,2,8,11,18,19,20,34,35,36,50]],axis=1,inplace=True)
	df.rename(columns={
	2: 'Off GP',
	3: '2PT',
	4: 'Comp',
	5: 'Pass Yds',
	6: 'Pass TD',
	7: 'Pass INT',
	9: 'Rush Yds',
	10: 'Rush TD',
	12: 'Rec',
	13: 'Rec Yds',
	14: 'Rec TD',
	15: 'Ret Yds',
	16: 'Ret TD',
	17: 'Fum Lost',
	21: 'K GP',
	22: '0-19 Made',
	23: '20-29 Made',
	24: '30-39 Made',
	25: '40-49 Made',
	26: '50+ Made',
	27: '0-19 Miss',
	28: '20-29 Miss',
	29: '30-39 Miss',
	30: '40-49 Miss',
	31: '50+ Miss',
	32: 'PAT Made',
	33: 'PAT Miss',
	37: 'Def GP',
	38: 'Pass Def',
	39: 'Blk Kick',
	40: 'Def Ret Yds',
	41: 'Def Ret TD',
	42: 'Tack Solo',
	43: 'Tack Ast',
	44: 'TFL',
	45: 'Sack',
	46: 'Safe',
	47: 'Def Int',
	48: 'Fum Force',
	49: 'Def TD'},inplace=True)
	raw_data.append(df)


totals = pd.concat(raw_data)

offense = pd.DataFrame(totals,columns=['Off GP','Comp','Pass Yds','Pass TD','Pass INT','Rush Yds','Rush TD','Rec','Rec Yds','Rec TD','Ret Yds','Ret TD','Fum Lost','2PT'])
offense.rename(columns={
	'Off GP' : 'GP',
	'Pass INT': 'INT'
	},inplace=True)
defense = pd.DataFrame(totals,columns=['Def GP','Pass Def','Blk Kick','Def Ret Yds','Def Ret TD','Tack Solo','Tack Ast','TFL','Sack','Safe','Def Int','Fum Force','Def TD'])
defense.rename(columns={
	'Def GP': 'GP',
	'Def Ret Yds' : 'Ret Yds',
	'Def Ret TD' : 'Ret TD',
	'Def INT' : 'INT'
	},inplace=True)
kicking = pd.DataFrame(totals,columns=['K GP','0-19 Made','20-29 Made','30-39 Made','40-49 Made','50+ Made','0-19 Miss','20-29 Miss','30-39 Miss','40-49 Miss','50+ Miss','PAT Made','PAT Miss'])
kicking.rename(columns={
	'K GP' : "GP"
	},inplace=True)

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)


sh = gc.open('2018 Naz 50/50')
wks = sh[5]
wks.set_dataframe(offense,(17,2))
wks.set_dataframe(defense,(32,2))
wks.set_dataframe(kicking,(47,2))
#wks.update_cell('M1',"Script completed on "+end+", took "+duration+" to run")