import json
import urllib, urllib2, cookielib, re, os, sys
import csv


def load_facebook_user(facebook_id):
	addy = 'http://graph.facebook.com/' + facebook_id
    	return json.load(urllib2.urlopen(addy))
i=1;
directory='/home/hoanghoa/facebookdata/user_profile/'
with open('friend_of_me.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
	data = load_facebook_user(row[0])
	with open(directory+row[0]+'.json', "w") as outfile:
		json.dump(data, outfile, sort_keys = True, indent = 4,ensure_ascii=True)
	print str(i) + ' user load completed'
	i=i+1

