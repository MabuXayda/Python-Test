import urllib, urllib2, cookielib, re, os, sys
from bs4 import BeautifulSoup
import json
import csv

class Acc:
    jar = cookielib.CookieJar()
    cookie = urllib2.HTTPCookieProcessor(jar)       
    opener = urllib2.build_opener(cookie)
    

    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
        "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "utf-8,ISO-8859-1",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "m.facebook.com"
    }
    
    
    def load_facebook_user(self,facebook_id):
	addy = 'http://graph.facebook.com/' + facebook_id
    	return json.load(urllib2.urlopen(addy))

    def login(self):
        try:
	    fl=[]
	    directory='/home/hoanghoa/facebookdata/test/'
    	    directoryFoF='/home/hoanghoa/facebookdata/test/'
            params = urllib.urlencode({'email':'hoanlongsu92@yahoo.com','pass':'hoanlongsu','login':'Log+In'})
            req = urllib2.Request('http://m.facebook.com/login.php?m=m&refsrc=m.facebook.com%2F', params, self.headers)
	    res = self.opener.open(req)

	    with open('me22.csv', 'rb') as lf:
	    	reader = csv.reader(lf)
		reader2=list(reader)
		for row in reader2[14:]:	    
	    	    user=  self.load_facebook_user(row[0])['username']
		    url = 'http://m.facebook.com/'+user+'?v=friends'
		    
		    while url!=None:		
			    print 'Collecting friends of '+user    
			    res2=self.opener.open(url)
			    html = res2.read()	
			    soup = BeautifulSoup(html)

			    if soup.find('div',{'class':'seeMoreFriends acw apm'})!=None:
				url ='http://m.facebook.com' + soup.find('div',{'class':'seeMoreFriends acw apm'}).find('a')['href']
			    else: url = None
						    
			    friends=soup.findAll('div',{'class':'_5pxa acw abt'})
			    for fr in friends:
				fl.append(fr.find('a')['href'].split('?')[0].split('/')[1])		    

		    print user + ' have ' + str(len(fl)) + ' friends'

		    user_id = self.load_facebook_user(user)['id']

		    with open(directoryFoF+user_id+'.csv', 'wb') as f:
			    writer = csv.writer(f) 
			    for friend in fl:
				try:
				    	data = self.load_facebook_user(friend)
					writer.writerow([data['id']])
					with open(directory+data['id']+'.json', "w") as outfile:
						json.dump(data, outfile, sort_keys = True, indent = 4,ensure_ascii=True)
					print data['id']+' FRIEND OF ' + user+ ' profile load completed'
				except: continue
		    print 'User '+user+' get friends Done'

        except urllib2.HTTPError, e:
            print e.msg
        except urllib2.URLError, e:
            print e.reason[1]
        return False

bla = Acc()
bla.login()


