#!/bin/bash

# THIS SCRIPT CONVERTS EVERY MP4 (IN THE CURRENT FOLDER AND SUBFOLDER) TO A MULTI-BITRATE VIDEO IN MP4-DASH
# For each file "videoname.mp4" it creates a folder "dash_videoname" containing a dash manifest file "stream.mpd" and subfolders containing video segments.
# Explanation: 
# https://rybakov.com/blog/

# Validation tool:
# http://dashif.org/conformance.html

# MDN reference:
# https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/Setting_up_adaptive_streaming_media_sources

# Add the following mime-types (uncommented) to .htaccess:
# AddType video/mp4 m4s
# AddType application/dash+xml mpd

# Use type="application/dash+xml" 
# in html when using mp4 as fallback:
#                <video data-dashjs-player loop="true" >
#                    <source src="/walking/walking.mpd" type="application/dash+xml">
#                    <source src="/walking/walking.mp4" type="video/mp4">
#                </video>

# DASH.js
# https://github.com/Dash-Industry-Forum/dash.js

MYDIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SAVEDIR=$(pwd)

# Check programs
if [ -z "$(which ffmpeg)" ]; then
    echo "Error: ffmpeg is not installed"
    exit 1
fi

if [ -z "$(which MP4Box)" ]; then
    echo "Error: MP4Box is not installed"
    exit 1
fi

cd "$MYDIR"

TARGET_FILES=$(find ./ -maxdepth 2 -type f \( -name "*.mov" -or -name "*.mp4" \))

for f in $TARGET_FILES
do
  fe="$f" # fullname of the file
  f="${fe%.*}" # name without extension
  base=$(basename "$f")

  echo "$f $fe $base"

  if [ ! -d "${f}" ]; then #if directory does not exist, convert
    echo "Converting \"$f\" to multi-bitrate video in MPEG-DASH"

    mkdir "${f}"

    ffmpeg -y -i "${fe}" -c:a libfdk_aac -ac 2 -ab 128k -c:v libx264 -x264opts 'keyint=24:min-keyint=24:no-scenecut' -b:v 1500k -maxrate 1500k -bufsize 1000k -vf "scale=-1:720"  "${f}720.mp4"

    ffmpeg -y -i "${fe}" -c:a libfdk_aac -ac 2 -ab 128k -c:v libx264 -x264opts 'keyint=24:min-keyint=24:no-scenecut' -b:v 800k -maxrate 800k -bufsize 500k -vf "scale=-1:540" "${f}540.mp4"

    ffmpeg -y -i "${fe}" -c:a libfdk_aac -ac 2 -ab 128k -c:v libx264 -x264opts 'keyint=24:min-keyint=24:no-scenecut' -b:v 400k -maxrate 400k -bufsize 400k -vf "scale=-1:360" "${f}360.mp4"

    rm -f ffmpeg*log*

    MP4Box -dash 1000 -rap -frag-rap  -bs-switching no -profile "dashavc264:live" "${f}720.mp4" "${f}540.mp4" "${f}360.mp4" -out "${f}/${base}.mpd"

  fi

done

cd "$SAVEDIR"