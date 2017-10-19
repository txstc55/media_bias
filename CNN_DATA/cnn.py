
import time
from bs4 import BeautifulSoup
from urllib2 import urlopen

import re
import requests
f=open('cnn_trump_url.txt','w')
for i in range(10,1000,10):
    time.sleep(8)
    url="https://www.google.com/search?q=donald+trump+site:cnn.com&start="+str(i)+"&cad=h"
    print i
    #print url
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    #print links
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #print link
        temp=re.split(":(?=http)",link["href"].replace("/url?q=",""))[0].split('&')[0]
        #print temp
        if 'webcache' not in temp:
            print temp
            f.writelines(temp+'\n')
f.close()
f=open('cnn_hillary_url.txt','w')
for i in range(10,620,10):
    time.sleep(8)
    url="https://www.google.com/search?q=hillary+clinton+site:cnn.com&start="+str(i)+"&cad=h"
    print i
    #print url
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    #print links
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #print link
        temp=re.split(":(?=http)",link["href"].replace("/url?q=",""))[0].split('&')[0]
        #print temp
        if 'webcache' not in temp:
            print temp
            f.writelines(temp+'\n')

f.close()