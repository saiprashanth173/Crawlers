
from getChannels import openPage
from bs4 import BeautifulSoup as bs
import json, re
import pymysql,urllib3
import requests
db = pymysql.connect('127.0.0.1','root','root','yt')
cursor = db.cursor(pymysql.cursors.DictCursor)
from multiprocessing import Pool

def openPageRequest(url):
    page = requests.get(url)
    return page.text
    
#open the required page
def openPage(url):
    http = urllib3.PoolManager()
    source = http.request('get',url)
    return source.data


#create required tables 
def createRequired():
    try:

        cursor.execute("CREATE TABLE IF NOT EXISTS main_links (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500),description VARCHAR(500), link VARCHAR(500) UNIQUE KEY,img_link VARCHAR(500),duration VARCHAR(30), duration_changed VARCHAR(100), channel_name VARCHAR(100), parent_channel VARCHAR(100))")
        cursor.execute("CREATE TABLE IF NOT EXISTS track_table (channel_link VARCHAR(500) PRIMARY KEY,next_link VARCHAR(500))")
        db.commit()

    except Exception as x:
        print (x)



# get content from sql 
def fetchContent():

    try:
        cursor.execute("SELECT sub_channel_name,sub_channel_link,parent_channel FROM channel_links WHERE crawled!=1 LIMIT 0,8")
        data = cursor.fetchall()
        return data
    except Exception as x:
        print (x)


#filter description i.e removes unwanted spaces
def filterContent(content):
    content = "".join(list(filter (lambda x: ord(x)>31 and ord(x)<128, content)))
    return re.sub("\s+"," ",content)


#stores the link details
def storeContent(data):
    try:
        print (data)
        cursor.execute("""INSERT INTO main_links(title, description, link,img_link ,duration , duration_changed , channel_name, parent_channel) VALUES %s"""%(str(data)))
        db.commit()
    except Exception as x:
        print (x)



    
#parse the given page
def parsePage(soup):
    open("content","w").write(str(soup))
    divs = soup.findAll('div',{'class':'yt-lockup-dismissable'}) 
    print (len(divs))
    dat= []
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
                description = filterContent(description).strip()
            except Exception as x:
                description = ""

            try:
                duration = div.find('span',{'class':'video-time'}).text
                changedDuration =  duration.replace(":","").strip()
            except :
                duration = ""
                changedDuration = ""
            
            linkTag = div.find('a')
            link = "https://www.youtube.com"+linkTag.attrs['href']
            title = div.find('h3').text
            title = filterContent(title).strip()
            dat.append((title,description,link,imgLink,duration,changedDuration))
            #storeContent((title,description,link,imgLink,duration,changedDuration,data["sub_channel_name"],data["parent_channel"]))
        except Exception as x:
            print (x)

    return dat

#gets link of the page to be crawled next
def getCallLink(soup):
    try:
        link = "https://www.youtube.com"+soup.find('button',{'class':re.compile('load-more-button')}).attrs['data-uix-load-more-href']
        return link
    except :
        return ""



# to keep track of completed records 
def updateTrack(link, next_link):
    try:
        if next_link == "":
            next_link = "completed"
        cursor.execute("INSERT INTO track_table VALUES ('%s','%s') ON DUPLICATE KEY UPDATE next_link='%s'" %(link,next_link,next_link))
        db.commit()
    except Exception as x:
        print (x)



#this involves identifying the ajax calls in first page 
def performStageOne(data):

    
    soup = bs(openPage(data["sub_channel_link"]))
    parsePage(data,soup)
    next_link = getCallLink(soup)
    updateTrack(data["sub_channel_link"],next_link)
    if next_link !="":
        performStageTwo(data,next_link)

    cursor.execute("UPDATE channel_links SET crawled=1 WHERE sub_channel_link = '%s'"%(data["sub_channel_link"]))
    db.commit()

#perform crawling from ajax calls
def performStageTwo(data,link):

    content = openPageRequest(link)
    open("store","w").write(content)
    jsonData = json.loads(content)
    parsePage(data,bs(jsonData["content_html"]))
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

    
    
#main function     
def main():
    
    createRequired()
    data = fetchContent()
    pool= Pool(8)
    pool.map(performStageOne,data)


#main()
