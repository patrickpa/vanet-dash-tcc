#!/bin/bash

MYDIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
SAVEDIR=$(pwd)

# Check programs
if [ -z "$(which ffmpeg)" ]; then
    echo "Error: ffmpeg is not installed"
    exit 1
fi

cd "$MYDIR"

TARGET_FILES="${3}${1}_src360.mp4 ${3}${1}_src540.mp4 ${3}${1}_src720.mp4"

echo "$TARGET_FILES"

for f in $TARGET_FILES
do
  fe="$f" # fullname of the file
  f="${fe%.*}" # name without extension
  base=$(basename "$f")

  echo "$f $fe $base"

  if [ ! -d "${f}" ]; then #if directory does not exist, convert
    echo "Cutting \"$fe\" into 1s pieces..."

    VID_DURATION=`ffmpeg -i "${fe}" 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print 3600*A[1] + 60*A[2] + B[1] }'`

    echo "Video Duration -> $VID_DURATION"

    mkdir "${f}"

    for i in $(seq 0 $VID_DURATION);
    do
        if $2 < 10
        then

            if $i < 10
            then
                ffmpeg -i "${fe}" -ss 00:00:0"$i" -t 00:00:0"$2" -async 1 "${f}/${i}_${base}.mp4"
            else
                ffmpeg -i "${fe}" -ss 00:00:"$i" -t 00:00:0"$2" -async 1 "${f}/${i}_${base}.mp4"
            fi

        else

            if $i < 10
            then
                ffmpeg -i "${fe}" -ss 00:00:0"$i" -t 00:00:"$2" -async 1 "${f}/${i}_${base}.mp4"
            else
                ffmpeg -i "${fe}" -ss 00:00:"$i" -t 00:00:"$2" -async 1 "${f}/${i}_${base}.mp4"
            fi
        fi

    done

    echo "All pieces cutted."

  fi

done
