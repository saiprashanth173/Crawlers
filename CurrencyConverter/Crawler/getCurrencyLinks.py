import MySQLdb
import config
import urllib2
from bs4 import BeautifulSoup as bs


db = MySQLdb.connect(config.host,config.user,config.passwd,config.db)

cursor= db.cursor()

#open the url and obtain soup object
def openPage(url):
    page = urllib2.urlopen(url)
    source = page.read()
    return bs(source)

#get currency links
def getLinks(url):
    soup = openPage(url)
    content= soup.find("ul",{"class":"currencyList"})
    links = content.findAll('a')

    for link in links:
        name = str(link.text).strip()
        link_to = str(link.attrs["href"]).strip()
        abbr = str(link_to.split("?from=")[1]).strip()
        storeValues((name,abbr,link_to))

#Store the content in MySQL
def storeValues(tup):
    try:
        sql = "INSERT INTO currency_links(currency_name,abbr,link) VALUES %s"%str(tup)
        #print sql
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x


getLinks("http://www.x-rates.com/")
