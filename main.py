import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from gpx_converter import Converter
import csv
 



json_file="log/"
altimet_json="log/1647853258.json"
altimet_json="log/16488334.json"
opend_json=open(altimet_json,'r')

alti_tim="Time"
alti_lat="Latitude"
alti_lon="Longitude"
alti_gpsalti="GPSAltitude"
alti_spd="Speed"
alti_lcp="Pressure"
alti_tem="Temperature"
alti_alt="Altitude"


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('station_data')

db_tim="sample_time"
db_slp="sea_lv_pressure"
db_lcp="local_pressure"
db_hum="humidity"
db_tem="temperature"

milliseconder=1

def scan_between(low_value,high_value):
    response = table.scan(
        FilterExpression=Attr(db_tim).between((low_value)-3000,high_value))


    return response

def query_eq():
    response = table.query(
        KeyConditionExpression=Key(db_tim).eq(1647800431647) and Key(db_tim).eq(1647800431647) )
    return response

def dic_to_list(dic):
    my_list=[]
    for var in dic:
        my_list.append(var)
    
    return my_list

def find_last(input):
    output=[]
    output.append(input[0][alti_tim])
    output.append(input[len(input)-1][alti_tim])
    return output
                
def sealv_to_altitude(slvp,altip,temp):

    cor_alti=((pow(slvp/altip,1/5.257)-1)*(temp+273.15))/0.0065
    
    return cor_alti
        
def calc_altitude(data_alti, data_station):
    time_in_station=0
    i=0
    newAlti=[]
    var=0

    for a in data_alti:

        time_in_alti=int(a[alti_tim]/milliseconder)
       


        if time_in_alti==time_in_station:
            i+=1

        if len(data_station)-1 >= i : 
            time_in_station=int(data_station[i][db_tim]/milliseconder)
        else:
            i=len(data_station)-1
            time_in_station=int(data_station[i][db_tim]/milliseconder)
        
        
        var+=1
        slp=float(data_station[i]["payload"][db_slp]/100)
        alp=float(a[alti_lcp])
        tmp=float(a[alti_tem])
        a[alti_alt]=round(sealv_to_altitude(slp, alp, tmp),2)
        newAlti.append(a)   

    return newAlti

alti_data=dic_to_list(json.load(opend_json))
timeinval=find_last(alti_data)

items=scan_between(timeinval[0], timeinval[1])['Items']
station_data=dic_to_list(sorted(items,key = lambda a: a[db_tim]))


def write_json(file_path, file_to_write):
    file_path +="log1.json"
    js_file=open(file_path,'a')
    js_file.write(json.dumps(file_to_write))

#write_json(json_file,calc_altitude(alti_data,station_data))
pre_json=calc_altitude(alti_data,station_data)

opendFile=open("log/log1.json",'r')
fieldnames=pre_json[0].keys()
 
with open('log/test.csv', mode='w') as csv_file:
    
        
    fieldnames=pre_json[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for a in pre_json:
         writer.writerow(a)
    

"""
Converter(input_file='log/16488334.json').csv_to_gpx(lats_colname=alti_lat,
                                                 longs_colname=alti_lon,
                                                 times_colname=alti_tim,
                                                 alts_colname=alti_alt,
                                                 output_file='log/test1.gpx')



"""
Converter(input_file="log/16488334.json").json_to_gpx(
                                                  lats_colname='Latitude',
                                                 longs_colname='Longitude',
                                                 times_colname=alti_tim,
                                                 alts_colname="Altitude",
                                                 output_file='log/your_output22.gpx')


print("program finished")                                                 