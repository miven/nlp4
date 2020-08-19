import datetime

now = datetime.datetime.strptime('2012-03-13', '%Y-%m-%d')
delta = datetime.timedelta(days=2*365)

tmp70 = (now + delta).strftime('%Y-%m-%d')
