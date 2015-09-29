import urllib2
from bs4 import BeautifulSoup as bs
import config
import json,months
import MySQLdb,threading
db= MySQLdb.connect(config.host,config.user,config.passwd,config.db)
cursor= db.cursor()
def openURL(url):
    print url
    page = urllib2.urlopen(url)
    source = page.read()
    return bs(source)

def getDates(date_number,month,year,number):
    lis=[]
    #print soup
    for day in range(date_number,months.months[str(month)]+1):
        link = "http://timesofindia.indiatimes.com/%s/%s/%s/archivelist/year-%s,month-%s,starttime-%s.cms"%(str(year),str(month),str(day),str(year),str(month),str(number))
        lis.append({"date":day,"year":year,"month":month,"link":link,"start":number})
        number+=1
    if int(year)%4==0 and int(month)==2:
        day=29
        link = "http://timesofindia.indiatimes.com/%s/%s/%s/archivelist/year-%s,month-%s,starttime-%s.cms"%(str(year),str(month),str(day),str(year),str(month),str(number))
        lis.append({"date":day,"year":year,"month":month,"link":link,"start":number})
    
    return lis


def getLinks(dicti):
    soup = openURL(dicti["link"])
    tables = soup.findAll('table')[2]
    links = tables.findAll('a')
    urls = []
    for link in links:
        try:
            url = link.attrs['href']
            url = url.split("//")[2]
            url = "http://timesofindia.indiatimes.com/"+url
            urls.append(url)
        except:
            pass
    return urls

def storeDB(tup):
    try:
        sql = "INSERT INTO page_content(`url`,`title`,`meta_description`,`body`,`tstamp`) VALUES %s"%str(tup)
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x

        
def storeContent(url,lis):
    content = openURL(url)
    body = ""
    try:
        body = str(content.find('div',{'id':'artext1'}).text)
    except :
        pass
    meta_description = ""
    try:
        meta_description = str(content.find('meta',{'name':'description'}).attrs['content'])
    except :
        pass
    title= str(content.find('title').text)
    if len(str(lis["month"]))<2:
        lis["month"]="0"+str(lis["month"])
    if len(str(lis["date"]))<2:
        lis["date"]="0"+str(lis["date"])
    storeDB((url,title,meta_description,body,str(lis["year"])+"-"+str(lis["month"])+"-"+str(lis["date"])+"T00:00:00.00Z"))
    
    
def crawlPages(lis):
    for li in lis:
        urls = getLinks(li)
        print urls
        threads = []
        for url in urls:
            try:
                t = threading.Thread(target=storeContent,args=(url,li))
                threads.append(t)
                #storeContent(url,li)
            except Exception as x:
                print x
        for thread in threads:
            while threading.active_count()>100:
                continue
            thread.start()
        for thread in threads:
            thread.join()
        k =open("track_file","w")
        if li["date"]>=months.months[str(int(li["month"]))]:
            month = li["month"]+1
        if month>12:
            month=1
            li["date"]=0
            li["year"]= li["year"]+1
            
        k.write(json.dumps({"day":li["date"]+1,"year":li["year"],"month":month,"start":li["start"]+1}))
        k.close()
def startOperation():
    k = json.load(open("track_file","r"))
    lis = getDates(k["day"],k["month"],k["year"],k["start"])
    crawlPages(lis)
startOperation()            
    
    
