import MySQLdb, config
import urllib2
from bs4 import BeautifulSoup as bs


#returns page source
def getSource(url):

    page= urllib2.urlopen(url)
    source = page.read()
    source = source.decode('unicode_escape').encode('ascii','ignore')

    return source

#parses the required page and 
def parsePage(soup):
    mainDiv = soup.find('div',{'id':'ikind--downloads'})
    videos = mainDiv.findAll('div',{'class':'item-ia'})

    for video in videos:
        try:
            ttl = video.find('div',{'class':'ttl C C2'})
            link = "https://archive.org"+ttl.find('a').attrs['href']
            title = filter(lambda x: ord(x)<128,ttl.text)
            title = title.strip()
            img = "https://archive.org"+video.find('img',{'class':'item-img'}).attrs['source']
            try:
                stats = video.findAll('h6',{'class':'stat'})
                views = str(stats[0].text).strip().replace(',','')
                fav = str(stats[1].text).strip().replace(',','')
            except :
                views = ''
                fav = ''

            print (link,title,views,fav,img)
        except Exception as x:
            print x
            pass

    channels = mainDiv.findAll('div',{'class':'item-ia collection-ia'})

    for channel in channels:
        link = "https://archive.org"+channel.find('a').attrs['href']
        print link
def performOperation():

    soup = bs(getSource("https://archive.org/details/movies?&sort=-downloads&page=2"))
    parsePage(soup)
        
        
        
