#run python
python3 get_recordings.py

#run batch download
./CNE_UNHAS_REKAMAN__A.sh
./CNE_UNHAS_REKAMAN__B.sh
./CCL_UNHAS_REKAMAN__A.sh
./CCL_UNHAS_REKAMAN__B.sh

#sync recording file with google drive
rclone copy CCNA/ ais:"Zoom Recordings"/"backup Recording"/CCNA/ -P
rclone copy CC/ ais:"Zoom Recordings"/"backup Recording"/CC/ -P

#delete recording file
rm /root/CC/"Kelas A"/*
rm /root/CC/"Kelas B"/*
rm /root/CCNA/"Kelas A"/*
rm /root/CCNA/"Kelas B"/*

#delete cloud recording 
python3 del_recordings.py

#sync attendance report with google drive
mv *.csv Zoom_Report

rclone copy Zoom_Report/ aisgmail:"20-FGA-Universitas Hasanuddin"/"Absensi"/"Zoom_Report" --drive-shared-with-me 

#delete bash file
rm /root/*UNHAS_REKAMAN*.sh
rm Zoom_Report/*.csv

