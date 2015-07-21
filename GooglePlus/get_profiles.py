import MySQLdb
import my_apikey as MAPI
import json
import urllib2
import config, conn

db = conn.db
db.select_db(config.db_name)
cursor = db.cursor()

def openPage(query,pageToken):
    url = "https://www.googleapis.com/plus/v1/people?query="+query.replace(" ","+")+"&maxResults=50&pageToken="+pageToken+"&key="+MAPI.api_key
    page = urllib2.urlopen(url)
    return page.read()

    

def getContent(jsonData):
    content = json.loads(jsonData)
    details =  content["items"]

    for detail in details:
        try:
            storeContent((str(detail["id"]),str(detail["objectType"]),str(detail["displayName"]),str(detail["url"]),str(detail["image"]["url"]),str(detail['etag'])))    
        except Exception as x:
            print x
            pass
    
    if "nextPageToken" in content :
        return content["nextPageToken"]
    else :
        return ""
    

def storeContent(content):
    try:
        sql = "INSERT INTO user_accounts (`id`,`type`,`display_name`,`link`,`img`,`tag`) VALUES %s"%(str(content))
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print sql
        print x
        
name = raw_input("Enter Name")
source = openPage(name,"")
src = getContent(source)

while src :
    source = openPage(name,src)
    src = getContent(source)

