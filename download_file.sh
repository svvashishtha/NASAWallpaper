#!/usr/bin/env bash

set -e
cd `dirname $0`



if [ $# -ne 2 ]; then
    echo "usage: wallpaper.sh <url> <filename>"
    exit 1
fi

url=$1
name=$2

filename="$HOME${name}"
echo $filename
# filename="$HOME/Pictures/random.jpg"
curl -L -o $filename $url

