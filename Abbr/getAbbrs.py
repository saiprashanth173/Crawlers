import urllib2
import MySQLdb
from bs4 import BeautifulSoup as bs
mapping_dicti = {"stage1":"(`link`,`category`)","stage2":"(`link`,`sub_category`,`category`)","stage3":"(`word`,`fullform`,`category`,`sub_category`)"}
db = MySQLdb.connect('127.0.0.1','root','root','kb_new')
cursor = db.cursor(MySQLdb.cursors.DictCursor)

def openUrl(url):
    page= urllib2.urlopen(url)
    source = page.read()
    source = filter(lambda x:ord(x)<128,source)
    return bs(source)

def storeContent(stage,content):
    try:
        sql = "INSERT INTO %s%s VALUES %s"%(stage,mapping_dicti[stage],content)
        print sql
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x

def parseStage1(soup):
    content = soup.find('div',{'id':'ctree'})
    headers = content.findAll('header')
    for header in headers:
        link= "http://www.abbreviations.com"+header.find('a').attrs['href']
        category = str(header.text).strip()
        storeContent("stage1",str((link,category)))

def performStage1():
    soup = openUrl("http://www.abbreviations.com/")
    parseStage1(soup)


def parseStage2(data):
    soup = openUrl(data["link"])
    content = soup.find('div',{'id':'content-body'})
    links= content.findAll('a')
    for link in links:
        subdomain = str(link.text).strip()
        url = link.attrs['href']
        storeContent("stage2",str((url,subdomain,data["category"])))
    
def parseStage3(data):
    count=data["counter"]
    print "http://www.abbreviations.com"+data["link"]+"/1"
    soup = openUrl("http://www.abbreviations.com"+data["link"]+"/"+str(count))
    content = soup.find('table',{'class':'table'})
    while content:
        trs = content.findAll('tr')
        if not trs:
            break
        for tr in trs:
            term= str(tr.find('td',{'class':'tm'}).text).strip()
            defin = str(filter(lambda x:ord(x)<128,tr.find('td',{'class':'dm'}).text)).strip()
            storeContent("stage3",str((term,defin,data["category"],data["sub_category"])))
        count+=1
        updateCounter(data["link"],count)
        print "http://www.abbreviations.com"+data["link"]+"/"+str(count)
        soup =openUrl("http://www.abbreviations.com"+data["link"]+"/"+str(count))
        content = soup.find('table',{'class':'table'})
    updateComplete(data["link"])

def updateComplete(link):
    try:
        sql = "UPDATE stage2 SET crawled='1' WHERE link='%s'"%(link)
        print sql
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x
        print "Exception in updating final update"


def updateCounter(link,count):
    try:
        sql = "UPDATE stage2 SET counter='%s' WHERE link='%s'"%(str(count),link)
        print sql
        cursor.execute(sql)
        db.commit()
    except:
        print "Exception in Update"
    
def performStage2():
    sql = "SELECT * FROM stage1 WHERE crawled=0"
    cursor.execute(sql)
    data = cursor.fetchall()
    for dat in data:
        parseStage2(dat)

def performStage3():
    sql = "SELECT * FROM stage2 WHERE crawled=0"
    cursor.execute(sql)
    data = cursor.fetchall()
    for dat in data:
        try:
            parseStage3(dat)
        except:
            pass


performStage3()

        
        
        
        
        

    
