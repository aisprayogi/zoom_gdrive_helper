import http.client
import json
#import re

import dateutil.parser
import os
import sys
import keys
import urllib.parse

def get_meeting_uuids(email, token):
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = { 'authorization': "Bearer "+ token}
    conn.request("GET", "/v2/users/"+email+"/recordings?trash_type=meeting_recordings&mc=false&page_size=30", headers=headers)

    res = conn.getresponse()
    data = res.read()

    uuids = []
    string = data.decode('utf-8')
    data = json.loads(string)
    if(data["total_records"]>0):
        meetings = data["meetings"]
        for meeting in meetings:
            uuids.append(meeting["uuid"])
    print(uuids)
    return uuids

def delete_recordings(email, token):
    uuids = get_meeting_uuids(email, token)
    for uuid in uuids:
        conn = http.client.HTTPSConnection("api.zoom.us")

        headers = { 'authorization': "Bearer "+ token}

        conn.request("DELETE", "/v2/meetings/"+ urllib.parse.quote(urllib.parse.quote(uuid,""),"") +"/recordings?action=trash", headers=headers)

        res = conn.getresponse()
        #print(urllib.parse.quote(urllib.parse.quote(uuid,""),""))
        print(res.status)
        #data = res.read()

        #print(data.decode("utf-8"))


delete_recordings(keys.email1, keys.token1)
delete_recordings(keys.email2, keys.token2)

