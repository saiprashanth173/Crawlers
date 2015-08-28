def parse(data):
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(data)
    data= "".join(result)
    parser.close()
    return data
import urllib2
import re
from HTMLParser import HTMLParser
import MySQLdb
import connection
db =connection.con()
cursor=db.cursor()
page=urllib2.urlopen("http://www.x-rates.com/table/?from=INR&amount=1.00")
data=page.read()
data=data.split("</table>")
data=data[1].split("<tbody>")
data=data[1].split("</tbody>")
tr=re.findall("<tr",data[0])
data="a"+data[0]
data=data.split("a",1)
for t in tr:
    a=[]
    for i in range(3):
        data=data[1].split("<td",1)
        data=data[1].split(">",1)
        data=data[1].split("</td>",1)
        cont=parse(data[0])
        a.append(cont)
    print a
    sql="SELECT * FROM `currency` WHERE `currency`='%s' "%(a[0])
    cursor.execute(sql)
    test=cursor.fetchall()
    if test==():
        sql="INSERT INTO `currency`(`currency`,`conv`,`invconv`) VALUES ('%s','%s','%s')"%(a[0],a[1],a[2])
        cursor.execute(sql)
        db.commit()
    else:
        sql1="UPDATE `currency` SET `currency`='%s',`conv`='%s',`invconv`='%s' WHERE `currency`='%s'"%(a[0],a[1],a[2],a[0])
        cursor.execute(sql1)
        db.commit()
db.close()
    
        
    
