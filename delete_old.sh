#!/usr/bin/env bash


set -e
cd `dirname $0`

if [ $# -ne 1 ]; then
    echo "usage: delte_old.sh <filename>"
    exit 1
fi

name=$1
filename="$HOME${name}"
echo "filename to delete"
echo $filename
rm $filename