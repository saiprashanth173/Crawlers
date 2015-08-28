import MySQLdb
import re
from bs4 import BeautifulSoup as bs

import connection
db=connection.con()

cursor=db.cursor()

import urllib2

def getLinksFromDb():

    sql = "SELECT url FROM weatherlinks"

    cursor.execute(sql)

    data= cursor.fetchall()

    return data

def openUrl(url):
    print url
    page=urllib2.urlopen(url)

    source=page.read()

    return source



def storeContent(contentList):

    contentList=[str(tuple(contentList))]+contentList

    sql = "INSERT INTO weather(`city`,`temperature`,`weather`,`feel`,`forecast`,`wind`,`visibility`,`pressure`,`humidity`,`dewpoint`) VALUES %s ON DUPLICATE KEY UPDATE `city`='%s',`temperature`='%s',`weather`='%s',`feel`='%s',`forecast`='%s',`wind`='%s',`visibility`='%s',`pressure`='%s',`humidity`='%s',`dewpoint`='%s' "%tuple(contentList)
    
    cursor.execute(sql)

    db.commit()


def getPageContent(place,source):

    soup=bs(source)
    getLis=temperatureDetails(soup)
    getLis+=getOtherDetails(soup)
    getLis=[place]+getLis
    storeContent(getLis)


def getOtherDetails(soup):
    otherDiv=soup.find('div',{'id':'qfacts'})
    contentList=map(makeChange,otherDiv.contents)
    contentList=contentList[contentList.index('<br/>')+1:]
    getLis=[]
    for content in contentList:
        soup=bs(content)
        p=soup.find('p')
        k=str(p.contents[1])
        getLis.append(k.strip())    
    return getLis


def makeChange(x2):
    return str(filter(lambda x:ord(x)<128,str(x2))).replace('C','')


    
def temperatureDetails(soup):
    tempDiv=soup.find('div',{'id':'qlook'})

    tempSoup=bs(str(tempDiv))

    temperature=tempSoup.find('div',{'class':'h2'}).text
    temperature= str(filter(lambda x: ord(x)<128,temperature).replace('C',''))
    ps=tempSoup.findAll('p')

    weatherContent=ps[0]
    weather=str(weatherContent.text).strip()
    otherWeather=ps[1]

    getDetail=str(otherWeather).split('<br/>')
    getLis=[]
    for get in getDetail:
        getLis.append(re.sub('<span.*</span>','',filter(lambda x : ord(x)<128,get.split(":")[1].strip().replace('</p>','').replace('C',''))))

    
    getLis=[temperature,weather]+getLis

    return getLis

def mainFun(option):
    links=list(getLinksFromDb())
    for link in links:
        try:
            place=link[0].split("/")
            place=place[len(place)-1].replace("-"," ")
            if option=="daily":
                source=openUrl(link[0])
                getPageContent(place,source)
            if option=="dailyext":
                source=openUrl(link[0]+"/ext")
                runDaily(place,source)
            elif option=="hourly":
                source=openUrl(link[0]+"/hourly")
                runHourly(place,source)
            
        
        except Exception as x:
            print x
            links.append(link)

def runHourly(place,source):
    sql ="DELETE FROM `weatherhourly` WHERE city='%s'"%(place)
    cursor.execute(sql)
    db.commit()
    soup=bs(source)
    table = soup.find('tbody')
    
    trs=table.contents
    
    for tr in trs:
        lis=[]
        contents=tr.contents
        for content in contents :
            if str(content.name)=='th':
                lis.append(str(str(filter(lambda x:ord(x)<128,content.text)).split(".")[0]).strip())
            
            elif '<span' not in str(content) and '<div' not in str(content) and 'img' not in str(content):
                lis.append(str(filter(lambda x:ord(x)<128,content.text)).strip().replace("C",""))
        lis=[place]+lis
        storeHourly(lis)
    #print lis

def runDaily(place,source):
    sql ="DELETE FROM `weatherforecast` WHERE city='%s'"%(place)
    cursor.execute(sql)
    db.commit()
    soup=bs(source)
    table = soup.find('tbody')
    
    trs=table.contents
    
    i=0
    for tr in trs:
        lis=[]
        i+=1
        contents=tr.contents
        j=0
        for content in contents :
            
            if str(content.name)=='th':
                
                lis.append(str(i))
            
            elif '<span' not in str(content) and '<div' not in str(content) and 'img' not in str(content):
                lis.append(str(filter(lambda x:ord(x)<128,content.text)).strip().replace("C",""))
            if(len(lis)==8):
                break
        lis=[place]+lis
        storeDaily(lis)
    
        if i==4:
            break



def storeHourly(lis):
    sql = "INSERT INTO weatherhourly VALUES %s"%str(tuple(lis))
    cursor.execute(sql)
    db.commit()


def storeDaily(lis):
    sql = "INSERT INTO weatherforecast VALUES %s"%str(tuple(lis))
    cursor.execute(sql)
    db.commit()



        

    

    

    
