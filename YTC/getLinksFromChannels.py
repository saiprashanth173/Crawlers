
import connection,urllib3
import pymysql
db = connection.db
cursor = db.cursor(pymysql.cursors.DictCursor)

from getChannels import openPage
from threading import Thread as T

def getFromDb():
    
    cursor.execute("SELECT channel_name,channel_link,type FROM channels WHERE crawled!=1")
    data= cursor.fetchall()

    return data


def createRequired():

    cursor.execute("CREATE TABLE IF NOT EXISTS channel_links (id INT AUTO_INCREMENT PRIMARY KEY, sub_channel_name VARCHAR(100), sub_channel_link VARCHAR(500) UNIQUE KEY,parent_channel VARCHAR(100), crawled INT DEFAULT 0)")
    db.commit()


def storeDatabase(content):
    try:
        cursor.execute("INSERT INTO channel_links (sub_channel_name, sub_channel_link,parent_channel) VALUES %s" %(str(content)))
        db.commit()
    except Exception as x:
        print (x)
        

def getLinks(data):
    
    try:
        soup = openPage(data["channel_link"])
        spans = soup.findAll('span',{'class':'qualified-channel-title-wrapper'})

        for span in spans:

            try:

                link= "https://www.youtube.com"+span.find('a').attrs['href']+"/videos"
                name = str(span.text).strip()
                storeDatabase((name,link,data["channel_name"]))

            except Exception as x:
                print (x)

        cursor.execute("UPDATE channels SET crawled = 1 WHERE channel_link = '%s' "%(data["channel_link"]))
        db.commit()

    except Exception as x:
        print (x)
        
def storeLinks(data):

    linkList = []
    
    if str(data["type"]) == "1":
        
        storeDatabase((data["channel_name"],data["channel_link"]+"/videos?flow=list",data["channel_name"]))
        cursor.execute("UPDATE channels SET crawled = 1 WHERE channel_link = '%s' "%(data["channel_link"]))
        db.commit()
        
    else :

        getLinks(data)
    
    
    
    
def main():

    createRequired()

    contents = getFromDb()
    for content in contents :
        T(target=storeLinks,args=(content,)).start()
    
    
    
main()
