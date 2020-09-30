import http.client
import json
import re

import dateutil.parser
import os
import sys
import keys
import urllib.parse
import csv


def get_meeting_infos(email, token):
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = { 'authorization': "Bearer "+ token}
    conn.request("GET", "/v2/users/"+email+"/recordings?trash_type=meeting_recordings&mc=false&page_size=30", headers=headers)

    res = conn.getresponse()
    data = res.read()

    meeting_infos = []
    string = data.decode('utf-8')
    data = json.loads(string)
    if(data["total_records"]>0):
        meetings = data["meetings"]
        for meeting in meetings:
            tanggal = dateutil.parser.isoparse(meeting["start_time"]).strftime("%m-%d")
            meeting_info = {"uuid": meeting["uuid"], "topic":meeting["topic"], "date":tanggal}
            meeting_infos.append(meeting_info)
    print(meeting_infos)
    return meeting_infos

def generate_report(meeting_info, token):
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = { 'authorization': "Bearer "+ token}
    conn.request("GET", "/v2/past_meetings/"+ urllib.parse.quote(urllib.parse.quote(meeting_info["uuid"],""),"") +"/participants?page_size=100", headers=headers)

    res = conn.getresponse()
    
    data = res.read()
    string = data.decode('utf-8')
    data = json.loads(string)
    participants = data["participants"]
    unique_participants = { each['name'] : each for each in participants }.values()
    #print(unique_participants)

    csv_columns = ['id','name','user_email']

    topic = re.sub('[^A-Za-z0-9 ]', '', meeting_info["topic"])
    csv_file = "./Zoom_Report/"+topic + "-" + meeting_info["date"]+".csv"

    if (os.path.isfile("./Zoom_Report/"+csv_file)):
        csv_file = "./Zoom_Report/"+topic + "-" + meeting_info["date"]+ "_1.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in unique_participants:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    

def delete_recordings(email, token):
    meeting_infos = get_meeting_infos(email, token)
    for meeting_info in meeting_infos:
        #generate participant meeting first
        generate_report(meeting_info,token)
        
        conn = http.client.HTTPSConnection("api.zoom.us")

        headers = { 'authorization': "Bearer "+ token}

        conn.request("DELETE", "/v2/meetings/"+ urllib.parse.quote(urllib.parse.quote(meeting_info["uuid"],""),"") +"/recordings?action=trash", headers=headers)

        res = conn.getresponse()
        #print(urllib.parse.quote(urllib.parse.quote(uuid,""),""))
        print(res.status)
        #data = res.read()

        #print(data.decode("utf-8"))


delete_recordings(keys.email1, keys.token1)
delete_recordings(keys.email2, keys.token2)

