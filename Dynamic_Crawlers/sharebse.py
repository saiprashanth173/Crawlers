def parse(data):
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(data)
    data= "".join(result)
    parser.close()
    return data
import re
import MySQLdb
import urllib2
from HTMLParser import HTMLParser
db=MySQLdb.connect('127.0.0.1','root','','prashanth')
cursor=db.cursor()
page=urllib2.urlopen("http://www.appuonline.com/b_bse30.html")
data=page.read()
data=data.split("<TABLE",1)
data=data[1].split("<tbody>",1)
data=data[1].split("</TABLE>",1)
data="a"+data[0]
data=data.split("a",1)
el=re.findall("<TR",data[1])
for e in el:
    data=data[1].split(e,1)
    data=data[1].split("</TR",1)
    td=re.findall("<TD",data[0])
    cont="a"+data[0]
    cont=cont.split("a",1)
    a=[]
    for t in td:
        cont=cont[1].split("<TD",1)
        cont=cont[1].split(">",1)
        cont=cont[1].split("</TD>",1)
        cont1=parse(cont[0])
        a.append(cont1)
    sql="SELECT * FROM `bse` WHERE `name`='%s'"%str(a[0])
    cursor.execute(sql)
    data1=cursor.fetchall()
    print data1
    
    if data1==():
        
        sql="INSERT INTO `bse`(`name`,`current`,`changep`,`prevclose`,`open`,`high`,`low`) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(a[0],a[1],a[2],a[3],a[4],a[5],a[6])
        cursor.execute(sql)
        db.commit()
    else:
        sql="UPDATE `bse` SET `current`='%s', `changep`='%s',`prevclose`='%s', `open`='%s', high='%s',low='%s'"%(a[1],a[2],a[3],a[4],a[5],a[6])
        cursor.execute(sql)
        db.commit()
        
        
        
    
