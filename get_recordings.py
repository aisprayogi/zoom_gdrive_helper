import http.client
import json
import re

import dateutil.parser
import os
import sys
import keys

def download_by_user(email, token):
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = { 'authorization': "Bearer "+ token}
    conn.request("GET", "/v2/users/"+email+"/recordings?trash_type=meeting_recordings&mc=false&page_size=30", headers=headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode('utf-8')
    data = json.loads(string)
    fileIndex = 0
    if(data["total_records"]>0):
        meetings = data["meetings"]
        for meeting in meetings:
            topic = meeting["topic"] 
            print(topic)
            tanggal = dateutil.parser.isoparse(meeting["start_time"])
            str_tanggal = tanggal.strftime("%d%m%Y")
            
            files = meeting["recording_files"]
            fileIndex = fileIndex + 1
            for file in files:
                if (file["recording_type"] == "shared_screen_with_speaker_view" ):
                    
                    print(fileIndex)
                    url_download = file["download_url"]+"?access_token="+token
                    #logging.info(url_download)
                    if(topic.startswith("Cloud A")):
                        file_prefix = "CCL_UNHAS_REKAMAN_"
                        file_suffix = "_A"
                        folder = "/root/CC/'Kelas A'/"
                    elif (topic.startswith("Cloud B")):
                        file_prefix = "CCL_UNHAS_REKAMAN_"
                        file_suffix = "_B"
                        folder = "/root/CC/'Kelas B'/"
                    elif (topic.startswith("CCNA A")):
                        file_prefix = "CNE_UNHAS_REKAMAN_"
                        file_suffix = "_A"
                        folder = "/root/CCNA/'Kelas A'/"
                    elif (topic.startswith("CCNA B")):
                        file_prefix = "CNE_UNHAS_REKAMAN_"
                        file_suffix = "_B"
                        folder = "/root/CCNA/'Kelas B'/"
                    else:
                        file_prefix = topic.replace(" ","_")
                        regex = re.compile('[^a-zA-Z]')
                        file_prefix = regex.sub('', file_prefix)
                        file_suffix = "_"+str(fileIndex)
                        if (email == "fga.unhas2@gmail.com"):
                            folder = "/root/CCNA/"
                        else:
                            folder = "root/CC/"
                    nama_file = file_prefix+str_tanggal+file_suffix
                    nama_skrip = file_prefix+ file_suffix +".sh" 
                    f = open(nama_skrip, "w")
                    f.write("wget -O "+ folder + nama_file + ".mp4 " + url_download)
                    f.close()
                    os.chmod(file_prefix+ file_suffix +".sh" , 0o755)


download_by_user(keys.email1, keys.token1)
download_by_user(keys.email2, keys.token2)