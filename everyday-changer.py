#!/usr/bin/env python3

from datetime import datetime
import subprocess
from os import path
import feedparser

DATE_FILE = "last-updated.conf"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

CACHE_FILE = "last-run.conf"


def set_background(filePath):
	script = """/usr/bin/osascript<<END
	tell application "Finder"
	set desktop picture to POSIX file "%s"
	end tell
	"""
	print (script)
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
	return subprocess.Popen(script%(filePath1,filePath2) , shell = True)

def delete_old_images():
	cache_file_path = path.join(path.abspath(path.dirname(__file__)), CACHE_FILE)
	

	try:
		filenames = tuple(open(cache_file_path, 'r'))
		for item in filenames:
			subprocess.run(["./delete_old.sh" ,item], cwd = path.abspath(path.dirname(__file__)))
	except IOError:
		print ("error opening cache conf file")

def write_cache(filename1, filename2):
	cache_file_path = path.join(path.abspath(path.dirname(__file__)), CACHE_FILE)
	with open(cache_file_path, "w") as f:
		f.write(filename1 + "\n" + filename2)


date_file_path = path.join(path.abspath(path.dirname(__file__)), DATE_FILE)

try:
    with open(date_file_path, "r") as f:
        last_date = datetime.strptime(f.readline().rstrip("\n"), DATE_FORMAT)
except IOError:
    last_date = datetime.fromtimestamp(0)

current_date = datetime.now()
if current_date.date() > last_date.date():
	feed = feedparser.parse('https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss')
	
	
	# download new files
	item = feed.entries[0]
	imgUrl = item.links[1].href

	filename1 = imgUrl.rpartition("/")[-1]
	filepath1  = "/Pictures/" + filename1 
	# download pic 1
	subprocess.run(["./download_file.sh", imgUrl ,filepath1], cwd = path.abspath(path.dirname(__file__)))
	
	item = feed.entries[1]
	imgUrl = item.links[1].href
	filename2 = imgUrl.rpartition("/")[-1]
	filepath2  = "/Pictures/" + filename2
	# download pic 2 
	subprocess.run(["./download_file.sh", imgUrl ,filepath2], cwd = path.abspath(path.dirname(__file__)))

	# set wallpaper here
	result = set_background_1(filepath1, filepath2)


	if not result.returncode:
		print ("I am hewre")
		delete_old_images()
		write_cache(filepath1, filepath2)
		with open(date_file_path, "w") as f:
			f.write(current_date.strftime(DATE_FORMAT))
