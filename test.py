from datetime import datetime, timedelta    

import time,calendar
epoch=int(1647853258)


def get_start_end_epch(inepoch):
    output=[]
    current_date=datetime.fromtimestamp(inepoch)
    output.append(calendar.timegm(time.strptime(str(current_date.date()), '%Y-%m-%d')))
    print()
    past_date = current_date - timedelta(hours=current_date.time().hour+1)
    output.append(calendar.timegm(time.strptime(str(past_date.date()), '%Y-%m-%d')))
    return output

print(get_start_end_epch(epoch))

"""
#print(ezis)
print("altimeter time: ")

for alma  in timeinval:
    humandate=datetime.datetime.utcfromtimestamp(alma/miliseconder).replace(tzinfo=datetime.timezone.utc)
    print(humandate)

print("dynamo database time:")

for alma  in station_data:
    my_epoch=int(alma[db_tim])/miliseconder 
    humandate=datetime.datetime.utcfromtimestamp(my_epoch).replace(tzinfo=datetime.timezone.utc)
    print(f'{humandate}: {alma["payload"][db_slp]}')
"""
