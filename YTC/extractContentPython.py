#coding=utf-8
#from getChannels import openPage
from bs4 import BeautifulSoup as bs
import json, re,JSONParser
import urllib3,unicodedata
import requests
import MySQLdb as pymysql
db = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
cursor = db.cursor(pymysql.cursors.DictCursor)
from multiprocessing import Pool

def openPageRequest(url):
    try:
        import urllib2
        url= url.replace("\/","/")
                         
        #page = requests.get(url)
        page = urllib2.urlopen(url)
        return page.read()
    except Exception as x:
        try:
            print x, [url]
            db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
            cursor =db1.cursor()
            cursor.execute("UPDATE track_table SET next_link = 'completed', next_link_nc='%s',status = 10 WHERE next_link= '%s'"%(str(url),url))
            db1.commit()
        except Exception as y:
            print y
#open the required page
def openPage(url):

    if "?flow=list" not in url:
        url= url+"?flow=list"
    
    http = urllib3.PoolManager()
    source = http.request('get',url)
    data = source.data
    #print (data)
    return data


#create required tables 
def createRequired():
    try:
        db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
        cursor =db1.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS main_links (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500),description VARCHAR(500), link VARCHAR(500) UNIQUE KEY,img_link VARCHAR(500),duration VARCHAR(30), duration_changed VARCHAR(100), channel_name VARCHAR(100), parent_channel VARCHAR(100))")
        cursor.execute("CREATE TABLE IF NOT EXISTS track_table (channel_link VARCHAR(500) PRIMARY KEY,next_link VARCHAR(500), next_link_nc VARCHAR(500), status int)")
        db1.commit()
        db1.close()
    except Exception as x:
        print (x)
        db1.close()



# get content from sql 
def fetchContent():

    try:
        db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
        cursor = db1.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT sub_channel_name,sub_channel_link,parent_channel FROM channel_links WHERE crawled!=1 LIMIT 0,8")
        data = cursor.fetchall()
        db1.close()
        return data
    except Exception as x:
        print (x)
        db1.close()



# get content from sql track
def fetchContentTrack():

    try:
        db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
        cursor =db1.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT channel_links.sub_channel_name as sub_channel_name,channel_links.sub_channel_link as sub_channel_link,channel_links.parent_channel as parent_channel,track_table.next_link as next_link FROM track_table INNER JOIN channel_links ON track_table.channel_link=channel_links.sub_channel_link WHERE next_link != 'completed'")
       
        data = cursor.fetchall()
        db1.close()
        return data
    except Exception as x:
        print (x)



#filter description i.e removes unwanted spaces
def filterContent(content):
    print (type(content))
    content = filter(lambda x: ord(x)>31 and ord(x)<128, str(content))
    #print (str(content))
    content = re.sub("\n+"," ",content)
    return re.sub("\s+"," ",content)


#stores the link details
def storeContent(data):
    try:
        db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
        cursor =db1.cursor()
     
        #print (data)
        cursor.execute("""INSERT INTO main_links(title, description, link,img_link ,duration , duration_changed , channel_name, parent_channel) VALUES %s"""%(str(data)))
        db1.commit()
        db1.close()
    except Exception as x:
        print (x)
        db1.close()



    
#parse the given page
def parsePage(data,soup):
    divs = soup.findAll('div',{'class':'yt-lockup-dismissable'}) 
    print (len(divs))
    for div in divs:
        try:
            try:
                imgLink = div.find('img').attrs['src']
                if "https:" not in imgLink:
                    imgLink = "https:"+imgLink
            except :
                imgLink = ""
            try:
                description = div.find('div',{'class':re.compile('yt-lockup-description')}).text
                description = str(filterContent(str(description)).strip())
            except Exception as x:
                description = ""

            try:
                duration = str(div.find('span',{'class':'video-time'}).text)
                changedDuration =  str(duration.replace(":","").strip())
            except :
                duration = ""
                changedDuration = ""
            
            linkTag = div.find('a')
            link = "https://www.youtube.com"+linkTag.attrs['href']
            link = link.replace("\/","/")
            title = div.find('h3').text
            title = filterContent(str(title)).strip()

            storeContent((title,description,link,imgLink,duration,changedDuration,data["sub_channel_name"],data["parent_channel"]))
        except Exception as x:
            print (x)



#gets link of the page to be crawled next
def getCallLink(soup):
    try:
        link = "https://www.youtube.com"+soup.find('button',{'class':re.compile('load-more-button')}).attrs['data-uix-load-more-href']
        link = link.replace("\/","/")
        return link
    except :
        return ""



# to keep track of completed records 
def updateTrack(link, next_link):
    try:
        db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
        cursor =db1.cursor()


        if next_link == "":
            next_link = "completed"
        cursor.execute("INSERT INTO track_table(channel_link,next_link) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE next_link='%s'" %(link,next_link,next_link))
        db1.commit()
        db1.close()
    except Exception as x:
        print (x)
        db1.close()



#this involves identifying the ajax calls in first page 
def performStageOne(data):

    content = filterContent(str(openPage(data["sub_channel_link"])))
    
    soup = bs(content)
    parsePage(data,soup)
    next_link = getCallLink(soup)
    updateTrack(data["sub_channel_link"],next_link)
    if next_link !="":
        performStageTwo(data,next_link)
    db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
    cursor =db1.cursor()


    cursor.execute("UPDATE channel_links SET crawled=1 WHERE sub_channel_link = '%s'"%(data["sub_channel_link"]))
    db1.commit()
    db1.close()
#perform crawling from ajax calls
def performStageTwo(data,link):
    
    content = openPageRequest(link)
#    print ("page Open")
   # open("store","w").write(content)
    try :

        content = content.decode('unicode_escape').encode('ascii','ignore')
        #content = unicodedata.normalize('NFDK',content).encode('ascii','ignore')
        #open("k","w").write(filterContent(content))
        #jsonData = json.loads(filterContent(content))
        jsonData = JSONParser.parseJson(filterContent(content))
        print "got json"
    #    print ("loaded content")
        parsePage(data,bs(filterContent(jsonData["content_html"])))
        print ("parsing completed")
        if ("load_more_widget_html" in jsonData):
            if (jsonData["load_more_widget_html"]):
                next_link = getCallLink(bs(jsonData["load_more_widget_html"]))
            else:
                next_link = ""
        else:
            next_link = ""
        
        updateTrack(data["sub_channel_link"],next_link)
        if next_link !="":
            performStageTwo(data,next_link)
    except Exception as x:
        print x,"Hello !"
        try:
            db1 = pymysql.connect("127.0.0.1","root","#srmseONserver1","yt")
            cursor =db1.cursor()
            cursor.execute("UPDATE track_table SET next_link = 'completed', next_link_nc='%s',status = 10 WHERE next_link= '%s'"%(str(link),link))
            db1.commit()
        except Exception as y:
            print y        
        
        
def startStageTwo(data):
    performStageTwo(data,data["next_link"])
    
#main function     
def main():
    
    while True: 
        try:
            print ("Creating tables")
            createRequired()
            print ("tables created")
            data = fetchContentTrack()
            print (data)
            if not data:
                data = fetchContent()
                if not data:
                    break
                pool= Pool(1)
                print (data)
                pool.map(performStageOne,data)
            else:
                pool = Pool(1)
                pool.map(startStageTwo,data)
                
        except Exception as x:
            print (x,"In main")
            pass
            


main()
