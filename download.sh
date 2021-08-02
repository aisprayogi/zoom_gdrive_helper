#!/bin/bash
set -e

python3 ./get_recordings.py

for f in ./scripts/*.sh; do
  bash "$f"
done

rclone copy --update --progress ~/zoom_gdrive/recording aisprayogiunhas:Rekaman

find ~/zoom_gdrive/recording -name "*.mp4" -type f -delete
find ~/zoom_gdrive/scripts -name "*.sh" -type f -delete

python3 ./del_recordings.py

rclone copy --update --progress ~/zoom_gdrive/Zoom_Report aisprayogiunhas:ZoomReport

find ~/zoom_gdrive/Zoom_Report -name "*.csv" -type f -delete
