import MySQLdb, config
import urllib2
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import threading
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

            storeContent("archive_videos",(str(link),str(title),str(views),str(fav),str(img)))
        except Exception as x:
            print x
            pass

    channels = mainDiv.findAll('div',{'class':'item-ia collection-ia'})

    for channel in channels:
        link = "https://archive.org"+channel.find('a').attrs['href']+"?&sort=-downloads&page="
        storeContent("archive_collections", link)
    if not channels and not videos:
        return False
    else:
        return True

def storeContent(table,content):
    try:
        db = MySQLdb.connect(config.host,config.user,config.paswd,config.db)
        cursor= db.cursor()
        if table == "archive_collections":
            sql = "INSERT INTO archive_collections(`link`,`present_link`) VALUES ('%s','1')"%str(content)
        elif table == "archive_videos":
            sql = "INSERT INTO archive_videos(`link`,`title`,`views`,`fav`,`img`) VALUES %s"%(str(content))
            
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x


def getFromDb():
    try:
        
        db = MySQLdb.connect(config.host,config.user,config.paswd,config.db)
        cursor= db.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM archive_collections WHERE `status`!='Done' "
        cursor.execute(sql)
        print sql
        data = cursor.fetchall()
        return data
    except Exception as x:
        print x


def getContent(data):
    db = MySQLdb.connect(config.host,config.user,config.paswd,config.db)
    cursor= db.cursor(MySQLdb.cursors.DictCursor)

    i =  int(data['present_link'])
        
    while True:
        
        link = data["link"] + str(i)
        
        soup = bs(getSource(link))
        if parsePage(soup):
            i = i+1
            cursor.execute("UPDATE archive_collections SET present_link= '%s' WHERE link = '%s' "%(i,data['link']) )
            db.commit()
        else:
            
            cursor.execute("UPDATE archive_collections SET status= 'done' WHERE link = '%s' "%(data['link']) )
            db.commit()
            break
    db.close()




def performOperation():
    data = getFromDb()
    for dat in data:
        while threading.active_count()>100:
            continue
        threading.Thread(target= getContent,args=(dat,)).start()
performOperation()        
        
        
