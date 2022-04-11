import matplotlib.pyplot as plt

import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('3wx_data')

def query_eq():
    response = table.query(
        KeyConditionExpression=Key('sample_time').eq(1647799832422))
    return response


def scan_grater():
    response = table.scan(
        FilterExpression=Attr('sample_time').gt(1647802015165))
    return response



def sort_items():
    my_list=[]

    for var in items:
       print(var["sample_time"])
       return var["sample_time"]

items=scan_grater()['Items']

sorted_list=sorted(items,key = lambda a: a["sample_time"])



time_table=[]
pres_table=[]

for var in sorted_list:
    
    humandate=datetime.datetime.utcfromtimestamp(int(var["sample_time"])/1000).replace(tzinfo=datetime.timezone.utc)
    time_table.append(humandate)
   
    pres_table.append(int(var["payload"]["pressure"]))




plt.plot_date(time_table, pres_table, fmt='o', tz=None, xdate=True, ydate=False,  data=None, color = 'g', 
             linestyle = 'dashed',marker = '.',label = "Weather Data")
  
plt.xticks(rotation = 0)
plt.xlabel('Dates')
plt.ylabel('Altitude [m]')
plt.title('Altitude Report', fontsize = 20)
plt.grid()
plt.legend()
plt.show()
