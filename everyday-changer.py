#!/usr/bin/env python3

from datetime import datetime
import subprocess
from os import path
import feedparser

def set_background(filePath):
	script = """/usr/bin/osascript<<END
	tell application "Finder"
	set desktop picture to POSIX file "%s"
	end tell
	"""
	return subprocess.Popen(script%filePath , shell = True)

def  set_background_1(filePath1, filePath2):
	filePath1 = "$HOME" + filePath1
	filePath2 = "$HOME" + filePath2
	script = """/usr/bin/osascript<<END
	tell application "System Events"
	set t to a reference to every desktop
	set picture of item 1 of t to POSIX file "%s" -- display 1
	set picture of item 2 of t to POSIX file "%s" -- display 2
	end tell"""
	print (script%(filePath1,filePath2))
	return subprocess.Popen(script%(filePath1,filePath2) , shell = True)


DATE_FILE = "last-updated.conf"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

date_file_path = path.join(path.abspath(path.dirname(__file__)), DATE_FILE)

try:
    with open(date_file_path, "r") as f:
        last_date = datetime.strptime(f.readline().rstrip("\n"), DATE_FORMAT)
except IOError:
    last_date = datetime.fromtimestamp(0)

current_date = datetime.now()
if current_date.date() > last_date.date():
	feed = feedparser.parse('https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss')
	item = feed.entries[0]
	imgUrl = item.links[1].href

	filename1 = imgUrl.rpartition("/")[-1]
	filepath1  = "/Pictures/" + filename1 

	subprocess.run(["./wallpaper.sh", imgUrl ,filepath1], cwd = path.abspath(path.dirname(__file__)))
	
	item = feed.entries[1]
	imgUrl = item.links[1].href
	filename2 = imgUrl.rpartition("/")[-1]
	filepath2  = "/Pictures/" + filename2 
	subprocess.run(["./wallpaper.sh", imgUrl ,filepath2], cwd = path.abspath(path.dirname(__file__)))
	result = set_background_1(filepath1, filepath2)


	# if not result.returncode:
	# 	with open(date_file_path, "w") as f:
	# 		f.write(current_date.strftime(DATE_FORMAT))
