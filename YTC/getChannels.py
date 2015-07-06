import connection

db = connection.dbFirst

from bs4 import BeautifulSoup as bs
import urllib3
import json,re

#create database
def createRequired():
    try:
        #create database if it doesnt exist 
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE yt")
        db.commit()
    except :
        print ("database exists")
        pass
    db.select_db("yt")
    cursor.execute("CREATE TABLE IF NOT EXISTS channels (id INT AUTO_INCREMENT PRIMARY KEY,channel_name VARCHAR(30) ,channel_link VARCHAR(60) UNIQUE KEY,type int,crawled INT DEFAULT 0) ")
    db.commit()

#open the required page
def openPage(url):
    http = urllib3.PoolManager()
    source = http.request('get',url)
    return bs(str(source.data))

# This is to get link of all available channels
def getChannels(soup):
    allChannels = []
    check = []
    hashLinks =  soup.findAll('li',{'id':re.compile('guide-item')})

    for hashLink in hashLinks:
        try:
            aTag = hashLink.find('a')
            channelName = str(aTag.text).replace("\\n","").strip()
            if channelName not in check :
                check.append(channelName)
                allChannels.append((channelName,"https://www.youtube.com"+aTag.attrs['href'],1))
        except Exception as x:
            print (x)
            
    allChannels= allChannels[1:len(allChannels)-1]    
    links = soup.findAll('a',{'class':'category-title-link'})
    
    for link in links:
        allChannels.append((link.text,"https://www.youtube.com"+link.attrs['href'],2))

    return allChannels

# store required channels 
def storeChannels(channels):

    cursor = db.cursor()
    sql = "INSERT INTO channels(channel_name,channel_link,type) VALUES %s "%(str(channels)[1:len(str(channels))-1])

    cursor.execute(sql)
    db.commit()
#calls all other functions

def main():

    createRequired()
    
    soup = openPage("https://www.youtube.com/channels") # returns bs object for page source

    channels =  getChannels(soup)

    storeChannels(channels)
    print (channels)

#main()
