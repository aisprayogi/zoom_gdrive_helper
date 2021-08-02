import http.client
import json
import re

import dateutil.parser
import os
import secrets


def download_by_user(dataAkun):
    # print(dataAkun)
    try:
        conn = http.client.HTTPSConnection("api.zoom.us")
        headers = {"authorization": "Bearer " + secrets.token}
        conn.request(
            "GET",
            "/v2/users/"
            + dataAkun["email"]
            + "/recordings?trash_type=meeting_recordings&mc=false&page_size=30",
            headers=headers,
        )

        res = conn.getresponse()
        data = res.read()

        string = data.decode("utf-8")
        data = json.loads(string)
        # print(data)
        fileIndex = 0
        if data["total_records"] > 0:
            # print(data["total_records"])
            meetings = data["meetings"]
            for meeting in meetings:
                topic = meeting["topic"]
                # print(topic)
                tanggal = dateutil.parser.isoparse(meeting["start_time"])
                str_tanggal = tanggal.strftime("%d%m%Y")

                files = meeting["recording_files"]
                for file in files:
                    # print(file)
                    if file["recording_type"] == "shared_screen_with_speaker_view":
                        # print(fileIndex)
                        url_download = (
                            file["download_url"] + "?access_token=" + secrets.token
                        )
                        # logging.info(url_download)
                        if topic.endswith(dataAkun["className"]):
                            file_prefix = (
                                dataAkun["temaCode"]
                                + "_UNHAS_REKAMAN_"
                                + str_tanggal
                                + "_"
                                + dataAkun["shortClassName"]
                            )
                            folder = (
                                "./recording/"
                                + dataAkun["temaCode"]
                                + "/"
                                + dataAkun["folderName"]
                                + "/"
                            )
                            if data["total_records"] > 1:
                                file_prefix += "_" + str(fileIndex)
                            nama_file = file_prefix
                            nama_skrip = "./scripts/" + file_prefix + ".sh"
                            f = open(nama_skrip, "w")
                            f.write(
                                'wget -O "'
                                + folder
                                + nama_file
                                + '.mp4" '
                                + url_download
                            )
                            f.close()
                            os.chmod(nama_skrip, 0o755)
                    fileIndex = fileIndex + 1
    except Exception as e:
        print(e)


# print("test")
for data in secrets.data:
    download_by_user(data)
