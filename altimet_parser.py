import csv
import calendar, time; 
import json

file="log/170322_17564900.csv"
json_file="log/"




#print(len(lines)

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

        time_in=time_in.replace("_","")
        day=time_in[0:2]
        month=time_in[2:4]
        year=time_in[4:6]

        hour=time_in[6:8]
        min=time_in[8:10]
        sec=time_in[10:12]
        milsec=time_in[12:14]

        new_time="20"+year+"-"+month+"-"+day+" "+hour+":"+min+":"+sec+"."+milsec
        new_time=calendar.timegm(time.strptime(new_time, '%Y-%m-%d %H:%M:%S.%f'))
        x["Time"]=new_time
        newList.append(x)
    
    return newList


valami=time_wizard(csv_to_dic(file))


#itiőt átnézni , milisec -->> sec re lett állítva!
def write_json(file_path, file_to_write):
    file_path +=str(valami[0].get("Time"))[:-2]+".json"
    js_file=open(file_path,'a')
    js_file.write(json.dumps(file_to_write))
    

def time_repalce(input_file):
    new_list=[]
    ezmeg=1648833410
    for az in input_file:    
        az["Time"]=ezmeg
        ezmeg+=1   
        new_list.append(az)
    return new_list

     
write_json(json_file,time_repalce(valami))

