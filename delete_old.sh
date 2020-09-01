#!/usr/bin/env bash


# set -e
# cd `dirname $0`

# if [ $# -ne 1 ]; then
#     echo "usage: delte_old.sh"
#     exit 1
# fi

# name=$1
echo $HOME
filename="${HOME}/Pictures/nasa/"
echo "deleting all pics from"
echo $filename
rm -v "$filename"