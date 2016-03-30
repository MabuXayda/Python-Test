import csv
import facebook
token='access token'
graph = facebook.GraphAPI(token)

profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

with open('friend_of_me.csv', 'wb') as f:
	writer = csv.writer(f)    
	for friend in friends['data']:
		writer.writerow([friend['id']])

#friend_list = [friend['id'] for friend in friends['data']]
print 'Load friends complete!'


