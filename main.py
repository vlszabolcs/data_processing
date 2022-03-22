import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import datetime



altimet_json="log/1647853258.json"
opend_json=open(altimet_json,'r')

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('3wx_data')

def scan_between(low_value,high_value):
    response = table.scan(
        FilterExpression=Attr('sample_time').between(low_value,high_value))
    return response

def query_eq():
    response = table.query(
        KeyConditionExpression=Key('sample_time').eq(1647800431647))
    return response


#items=query_eq()['Items']
#items=scan_between(1647879163502,1647881863571)['Items']


def dic_to_list(dic):
    my_list=[]

    for var in dic:
        my_list.append(var)
    return my_list

def find_last(input):
    output=[]
    output.append(input[0]["Time"])
    output.append(input[len(input)-1]["Time"])
    return output

alti_data=dic_to_list(json.load(opend_json))
timeinval=find_last(alti_data)

items=scan_between(timeinval[0], timeinval[1])['Items']
ezis=dic_to_list(items)


for alma in ezis:
    epoch=int(alma["sample_time"]) 
    print(epoch)
    humandate=datetime.datetime.utcfromtimestamp(epoch).replace(tzinfo=datetime.timezone.utc) #SZAR! NEM működik
    print(humandate)

 

  


        