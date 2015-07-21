import connection
import re
from threading import Thread
import MySQLdb
def parsePage(soup,channel):
    print soup
    videos = soup.findAll('div',{'class':re.compile('sd_video_listitem')})
    if not videos:
        videos = soup.findAll('div',{'class':re.compile('sd_video_griditem')})
    for video in videos:
        print video.findAll('img')
        img = video.find('img').attrs['data-src']
        try:
            duration = video.find('div',{'class':re.compile('duration')}).text
            duration = str(duration.strip())
            changedDuration = str(duration.replace(":",""))
        except:
            duration = ""
            changedDuration = ""
        contentDiv = video.find('div',{'class':'media-block'})
        
        linkTag = contentDiv.find('a')
        link = str("http://www.dailymotion.com"+linkTag.attrs['href'])
        title = str(linkTag.attrs['title'].strip())

        try :
            owner = contentDiv.find('div',{'class':'owner'}).text
            owner = str(owner.strip())
        except:
            owner = ""

        title = title + " " + owner
        title = str(title.strip())

        storeContent((link,title,img,duration,changedDuration,channel))

def storeContent(cont):

    try :
        
        import connection_main
        db = connection_main.db
        cursor= db.cursor(MySQLdb.cursors.DictCursor)
        print cont
        cursor.execute("INSERT INTO main_links(link,title,img_link,duration,duration_changed,channel_name) VALUES %s"%(str(cont)))
        db.commit()
        #db.close()
    except Exception as x:
        #db.close()
        print x


def getFromTrack():
    import connection_main
    db = connection_main.db
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT next_link,channel_name FROM track_table WHERE next_link!='completed' limit 0,1")
    data = cursor.fetchall()
    return data

def getFromChannels():
    import connection_main
    db = connection_main.db
    cursor=db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT channel_link,channel_name FROM channels WHERE crawled!=1 limit 0,1")
    data = cursor.fetchall()
    return data
    

def startParser(count,link,channel):

    for i in range(count,101):
        try:

            parsePage(connection.getPageSource(link+"/"+str(i)),channel)

            sql = "INSERT INTO track_table(`channel_name`,`next_link`) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE next_link='%s'"%(channel,link+"/"+str(i+1),link+"/"+str(i+1))

            print sql
            import MySQLdb
            db = MySQLdb.connect('127.0.0.1','root','root','dailymotion')
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
        except Exception as x:
            print x
            cursor.execute("INSERT INTO track_table(`channel_name`) VALUES ('%s') ON DUPLICATE KEY UPDATE next_link_nc='%s',next_link='completed' ,status=10"%(channel,link+"/"+str(count)))
        db.commit()
    import MySQLdb
    db = MySQLdb.connect('127.0.0.1','root','root','dailymotion')
    cursor = db.cursor()
    sql = "INSERT INTO track_table(`channel_name`,`next_link`) VALUES ('%s','completed') ON DUPLICATE KEY UPDATE next_link='completed'"%(channel)
    cursor.execute(sql)
    db.commit()
    
def main():
    data =getFromTrack()
    import connection_main as con
    db = con.db
    cursor= db.cursor()
    if data:
        for dat in data:
            content = dat['next_link'].rsplit('/',1)
            count = int(content[1])
            startParser(count,content[0],dat['channel_name'])
            cursor.execute("UPDATE channels SET `crawled`=1 WHERE channel_name= '%s'"%(dat['channel_name']))
            db.commit()
    else:
        data = getFromChannels()
        if data:
            for dat in data:
                startParser(1,dat['channel_link'],dat['channel_name'])
                cursor.execute("UPDATE channels SET `crawled`=1 WHERE channel_name= '%s'"%(dat['channel_name']))
                db.commit()
