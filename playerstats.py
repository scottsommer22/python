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

url = 'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=0'

urls = [
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=0',
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=200',
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=400',
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=600',
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=800',
'https://www.hockey-reference.com/play-index/psl_finder.cgi?c2stat=&c4stat=&c2comp=gt&is_playoffs=N&order_by_asc=&birthyear_max=&birthyear_min=&c1comp=gt&year_min=&request=1&franch_id=&is_hof=&birth_country=&match=combined&year_max=&c3comp=gt&season_end=-1&is_active=Y&c3stat=&lg_id=NHL&order_by=goals&season_start=1&c1val=&threshhold=5&c3val=&c2val=&am_team_id=&handed=&rookie=N&pos=S&describe_only=&c1stat=&draft=&c4val=&age_min=0&c4comp=gt&age_max=99&offset=1000']

array = []
for i in urls:
	data = pd.read_html(i)[0]
	data.columns = range(data.shape[1])
	df = pd.DataFrame(data).set_index(0).reset_index().fillna('-')
	df.rename(columns={
	0: 'Rank',
	1: 'Player',
	2: 'Goals',
	3: 'Tm',
	4: 'Pos',
	5: 'From',
	6: 'To',
	7: 'Active',
	8: 'GP',
	9: 'A',
	10: 'PTS',
	11: '="+/-"',
	12: 'PIM',
	13: 'EV',
	14: 'PP',
	15: 'SH',
	16: 'GW',
	17: 'S',
	18: 'S%',
	19: 'TOI',
	20: 'GPG',
	21: 'APG',
	22: 'PPG',
	23: 'SPG',
	24: 'OPS',
	25: 'DPS',
	26: 'PS',
	27: 'G_Adj',
	28: 'A_Adj',
	29: 'PTS_Adj'},inplace=True)
	
	del df['Rank']

	array.append(df)

x = pd.concat(array)

fmt = "%m/%d/%Y at %I:%M:%S %p"
end = datetime.now(timezone('US/Eastern'))
end = end.strftime(fmt)

duration = str(datetime.now() - start)

#print df
sh = gc.open('CapSpace Data')
wks = sh[7]
wks.set_dataframe(x,(1,1))
#wks.update_cell('M1',"Script completed on "+end+", took "+duration+" to run")