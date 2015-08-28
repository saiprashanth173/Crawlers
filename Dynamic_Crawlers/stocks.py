from bs4 import BeautifulSoup as bs


import urllib2
import MySQLdb
import connection

db =connection.con()
cursor=db.cursor()

def openPage(url):
    
    page = urllib2.urlopen(url)

    source = page.read()

    return source


def parsePage(source,typ):

    soup=bs(source,"html.parser")

    table=soup.find("table",{"class":"dataTable"})

    soup=bs(str(table),"html.parser")

    tbody=soup.find("tbody")

    soup=bs(str(tbody),"html.parser")

    trs=soup.findAll("tr")
    for tr in trs:
        lis=[]
        soup=bs(str(tr),"html.parser")

        tds=soup.findAll("td")

        for td in tds:

            lis.append(str(td.text).strip().replace("'",''))
        storeDB(lis,typ)


def storeDB(lis,typ):
    if typ=="bse":
        lis.pop(1)
    a=tuple(lis)
    sql="INSERT INTO "+typ+"(`company`,`prev_cost`,`current_price`,`per_change`) VALUES "+str(tuple(lis))+" ON DUPLICATE KEY UPDATE `company`='%s',`prev_cost`='%s',`current_price`='%s',`per_change`='%s'"%a
   # print sql
	 #print sql
    cursor.execute(sql)
    db.commit()
    
def mainFun(typ):
    typlis=["losers","gainers"]
    if typ=="nse":
        for tp in typlis:
            print "---------"+tp+"-----------"
            url="http://money.rediff.com/"+tp+"/nse"
            source=openPage(url)
            parsePage(source,typ)
    else:
        for tp in typlis:
            print "---------"+tp+"-----------"
            url="http://money.rediff.com/"+tp+"/bse"
            source=openPage(url)
            parsePage(source,typ)
        
            


            

            

        

        

        

    
