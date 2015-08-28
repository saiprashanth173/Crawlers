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
import connection
db=connection.con()
cursor=db.cursor()
parser = HTMLParser()

page=urllib2.urlopen("http://www.runningstatus.in/")
data=page.read()
data=data.split('<div class="runningstatus-activity-feeds">',1)
data=data[1].split('<ul>',1)
data=data[1].split('</ul>',1)
test=re.findall('<li>',data[0])
data="a"+data[0]
data=data.split("a",1)
tes=[]

try:
    for te in test:
        data=data[1].split('<div class="text">',1)
        data=data[1].split('<p>',1)
        data=data[1].split('</span>',1)
        name=parse(data[0])
        num=name.split('(',1)
        name=num[0].strip()
        num=num[1].split(')',1)
        data=data[1].split('</p>',1)
        text=data[0]
        data=data[1].split('</span>',1)
        data=data[1].split('</span>',1)
        status=parse(data[0])
        status=status.split('\n',1)
        print "\nTrain Name: "+name
        print "Number: "+num[0]
        print "Text: "+text
        print "Short Status: "+status[0]
        print "Status: "+status[1].strip()
        status[1]=status[1].strip()
        sql="SELECT `text` FROM `train` WHERE `trainnum`='%d'"%(int(num[0]))
        cursor.execute(sql)
        row=cursor.fetchall()
        if str(row)!="()":
            date=re.findall('([0-9]{1,2})[a-z]{2}',row[0][0])
            datet=re.findall('([0-9]{1,2})[a-z]{2}',text)
            print datet[0]
            print date[0]
            if int(datet[0])==int(date[0]):
                sql="UPDATE `train` SET `text`='%s',`sstatus`='%s',`lstatus`='%s' WHERE `trainnum`='%d'"%(str(text),str(status[0]),str(status[1]),int(num[0]))
               # cursor.execute(sql)
                db.commit()
            if (int(datet[0])>int(date[0]) or (int(date[0])-int(datet[0]))>7) and (int(datet[0])-int(date[0]))<20:
                print "greater loop"
                sql="SELECT `text`,`sstatus`,`lstatus`,`text1`,`sstatus1`,`lstatus1`,`text2`,`sstatus2`,`lstatus2` FROM `train` WHERE trainnum='%s'"%str(num[0])
                cursor.execute(sql)
                change=cursor.fetchall()
                text1=change[0][0]
                sstatus1=change[0][1]
                lstatus1=change[0][2]
                text2=change[0][3]
                sstatus2=change[0][4]
                lstatus2=change[0][5]
                text3=change[0][6]
                sstatus3=change[0][7]
                lstatus3=change[0][8]
                sql="UPDATE `train` SET `text`='%s',`sstatus`='%s',`lstatus`='%s',`text1`='%s',`sstatus1`='%s',`lstatus1`='%s',`text2`='%s',`sstatus2`='%s',`lstatus2`='%s',`text3`='%s',`sstatus3`='%s',`lstatus3`='%s' WHERE `trainnum`='%s'"%(str(text),str(status[0]),str(status[1]),text1,sstatus1,lstatus1,text2,sstatus2,lstatus2,text3,sstatus3,lstatus3,str(num[0])) 
                cursor.execute(sql)
                db.commit()
            elif int(datet[0])<int(date[0]):
                print "lesser group"
                a=int(date[0])-int(datet[0])
                if int(date[0])-int(datet[0])>3:
                    a=3
                sql="UPDATE `train` SET `text%d`='%s',`sstatus%d`='%s',`lstatus%d`='%s' WHERE `trainnum`='%d'"%(int(a),str(text),int(a),str(status[0]),int(a),str(status[1]),int(num[0]))
                cursor.execute(sql)
                db.commit()
            elif int(datet[0])-int(date[0])>20:
                print "change in month"
                sql="SELECT text1 from train where trainnum='%s'"%(str(num[0]))
                cursor.execute(sql)
                data111=cursor.fetchall()
                content=re.findall('([0-9]{1,2})[a-z]{2}',data111[0][0])
                
                a=int(content[0])+int(date[0])-int(datet[0])
                sql="UPDATE `train` SET `text%d`='%s',`sstatus%d`='%s',`lstatus%d`='%s' WHERE `trainnum`='%s'"%(int(a),str(text),int(a),str(status[0]),int(a),str(status[1]),str(num[0]))
                cursor.execute(sql)
                db.commit()
            
                
                
                
                
        else: 
            sql="INSERT INTO `train`(`trainnum`,`trainname`,`text`,`sstatus`,`lstatus`) VALUES ('%s','%s','%s','%s','%s')"%(int(num[0]),str(name),str(text),str(status[0]),str(status[1]))
            cursor.execute(sql)
            db.commit()
       
except Exception as x:
        print x

    
    


