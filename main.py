from lib2to3.pytree import convert
import boto3
import calendar,time
from boto3.dynamodb.conditions import Key, Attr
import json
import csv

import pandas as pd


 

altimet_csv="test2/2022412165649.csv"

alti_tim="Time"
alti_lat="Latitude"
alti_lon="Longitude"
alti_gpsalti="GPSAltitude"
alti_spd="Speed"
alti_lcp="Pressure"
alti_tem="Temperature"
alti_alt="Altitude"


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('station_test2')

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

def csv_to_dic(filename):
    dic=[] 
    with open(filename, 'r') as data:  
        for line in csv.DictReader(data):
            dic.append(line)
    return dic
   
def time_wizard(old_list):
    newList=[]

    for x in old_list:
        time_in=x.get("Time")
     
        new_time=time_in
        new_time=calendar.timegm(time.strptime(new_time, '%Y%m%d%H%M%S'))
        

        
        x["Time"]=new_time
        newList.append(x)

    return newList


def dataframe_to_gpx(input_df, output_file=None):
        """
        convert pandas dataframe to gpx
        input_df: pandas dataframe
        lats_colname: name of the latitudes column
        longs_colname: name of the longitudes column
        times_colname: name of the time column
        alts_colname: name of the altitudes column
        output_file: path of the output file
        """
        import gpxpy.gpx
        gpx = gpxpy.gpx.GPX()


        lats_colname=alti_lat,
        longs_colname=alti_lon,
        times_colname=alti_tim,
        alts_colname=alti_alt,

        json_df = []
        json_df=pd.read_json(input_df)
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        for idx in json_df.index:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(json_df.loc[idx, lats_colname],
                                                              json_df.loc[idx, longs_colname],
                                                              time=pd.to_datetime(json_df.loc[idx, times_colname],unit='s') if times_colname else None,
                                                              elevation=json_df.loc[idx, alts_colname] if alts_colname else None))
        
        with open(output_file, 'w') as f:
            f.write(gpx.to_xml())
        return gpx.to_xml()

alti_data=time_wizard(csv_to_dic(altimet_csv))
#alti_data=dic_to_list(alti_data)
originalAlti=dataframe_to_gpx(json.dumps(alti_data),"test2/orig_alti.gpx")

#alti_data=dic_to_list(alti_data)
#alti_data=dic_to_list(json.load(opend_json))

timeinval=find_last(alti_data)
items=scan_between(timeinval[0], timeinval[1])['Items']
station_data=dic_to_list(sorted(items,key = lambda a: a[db_tim]))

pre_json=calc_altitude(alti_data,station_data)
modAlti=dataframe_to_gpx(json.dumps(pre_json),"test2/mod_alti.gpx")

print("program finished")                                                 