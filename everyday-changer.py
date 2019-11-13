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
	subprocess.run(["./wallpaper.sh", imgUrl], cwd = path.abspath(path.dirname(__file__)))
	result = set_background("$HOME/Pictures/random.png")
	if not result.returncode:
		with open(date_file_path, "w") as f:
			f.write(current_date.strftime(DATE_FORMAT))
