import json
import urllib2
import pymongo
#from pymongo import Connection
import csv
import os

#connection = Connection()
#connection = Connection('localhost', 27017)
#db = connection.mydb
#collection = db.user_data

def load_feeddata(url):
	try:
	    return json.load(urllib2.urlopen(url))
	except urllib2.HTTPError, e:
            print e.msg
        except urllib2.URLError, e:
            print e.reason[1]
user_count=1
directory='/home/hoanghoa/facebookdata/user_data/'
access_token='CAACEdEose0cBAGubHRtq4XkXewYnUxsTu7leZB4zMk9UGKTeE6OW8Fz6FAZCXzG1HiwtaGRZBWZAsimfmsGzcvIuBY84ZC4lMiEIWX17mgGpnmhqnwazjYrj9MAVgZCuxZAyDLAeeu4IWgsZBl4L67eUZBGjnqzwqZC99UNmsY9DJQKwcK260o7ZBKM9NW8lZAAYZB9v7n63kFZAKKIgZDZD'

with open('me22.csv', 'rb') as f:
    	reader = csv.reader(f)
	reader2=list(reader)
	for row in reader2:
		try:
			print user_count
			feed_count = 1
			userid=row[0]
			link='https://graph.facebook.com/'+userid+'/feed?access_token='+access_token
			while link!=None:
				try:
					data = load_feeddata(link)
					#if data == Null: break
					dr=directory+userid					
					if not os.path.exists(dr):
						os.makedirs(dr)
					filename=dr+'/'+userid+'_'+str(feed_count)+'.json'					
					with open(filename, 'w') as outfile:
						json.dump(data, outfile, sort_keys = True, indent = 4,ensure_ascii=True)
					print 'user '+ str(user_count)+' '+ str(feed_count) + ' feed of '+ userid +' completed...'
					if data.get("paging") is not None:
						link= data["paging"]["next"]
					else: link = None
					feed_count = feed_count + 1
				except IOError as e:
			    		print "I/O error({0}): {1}".format(e.errno, e.strerror) 
			print 'Crawl ' + userid +' complete'
			user_count = user_count + 1			
		except:
			print userid + ' crawl failed!'
			user_count = user_count + 1
			continue
			
print "Crawl completed"
	
#print_feeddata('598688231','CAACEdEose0cBAG6Lh9kN1PpPlsVUs8ohGkfXtv69FZCRz4tfZCm26lEKXUB9LZCtEYzF93TqA51heTEKH1QyZA1OF9CuQ9BcpocUVXK0Wt2PlAqyq7p0T3Tcs8ZCUgKq1uh8XnJ87pR9s4FOKLWhsXZBbsCqOqTdqQOeZCsiFP7DnO0ZAEbzCXijlbdneuKQE4tuedAggUjCYwZDZD')
