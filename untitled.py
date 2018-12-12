url = 'http://www.naturalstattrick.com/teamtable.php?season=20132014&stype=1&sit=5v5&score=all&rate=n&vs=all&loc=B&fd=2018-09-15&td=2018-10-03'

x = url.split("season=")[1].split("&")[0][-4:]

print x