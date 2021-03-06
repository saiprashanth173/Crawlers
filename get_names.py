import urllib2

import MySQLdb

from bs4 import BeautifulSoup as bs

def getSource(num):
    url = "http://www.name-list.net/facebook/"+num
    page = urllib2.urlopen(url)
    f=open("check","a")
    f.write(str(num)+"\n")
    f.close()
    return page.read()


def storeContent(name):
    db = MySQLdb.connect('127.0.0.1','root','root','google_plus')

    cursor = db.cursor()

    name = filter(lambda x:ord(x)<128,name)
    name = name.strip()
    try:
        sql = "INSERT INTO names(`name`) values ('%s')"%(name)
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        pass

        #print x

    names = name.split()

    for nam in names:
        try:
            sql = "INSERT INTO names_single(`name`) values ('%s')"%(nam)
            cursor.execute(sql)
            db.commit()
        except Exception as x:
            pass
            #print x
    db.close()

def parsePage(soup):
    table = soup.find('table',{'class':'list'})
    trs = table.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        for td in tds:
            storeContent(td.text)

def startCrawling(num):
    page = bs(getSource(str(num)))
    parsePage(page)
    
def main():
    import threading
    for i in range(44955,95001):
        
        print i
        while threading.active_count()>400:
            continue
        
        threading.Thread(target=startCrawling,args=(i,)).start()        
main()
