import pymongo
client = pymongo.MongoClient()
from bs4 import BeautifulSoup as bs
import MySQLdb
import config
import urllib2

db = MySQLdb.connect(config.host,config.user,config.passwd,config.db)
cursor= db.cursor(MySQLdb.cursors.DictCursor)
mapping = {}

def getMapping(values):
    for value in values:
        mapping[value["currency_name"]]=value["abbr"]
    print mapping.keys()
#get from db
def getFromDb():
    cursor.execute("SELECT * FROM currency_links")
    return list(cursor.fetchall())


#open the url and obtain soup object
def openPage(url):
    page = urllib2.urlopen(url)
    source = page.read()
    return bs(source)

# obtain content
def parsePage(values):
    url = values["link"]
    soup = openPage(url)
    print values
    content = soup.find('table',{"class":'tablesorter'})
    table = content.find('tbody')
    trs = table.findAll('tr')
    content = {"name":values["currency_name"],"short_name":values["abbr"],"convert":{}}
    for tr in trs:
        try:
            values= tr.findAll('td')
            name = str(values[0].text).strip()
            value = str(values[1].text).strip()
            content["convert"][name] = value
            content["convert"][mapping[name]] = value
        except Exception as x:
            print x
    storeContent(content)

#store content in mongodb
def storeContent(content):
    db = client.currencydb
    db.currency.update({"name":content["name"]},content,True)

def main():
    data= getFromDb()
    getMapping(data)
    for dat in data:
        parsePage(dat)
main()
