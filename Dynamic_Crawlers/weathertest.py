import urllib2
import re
import datetime
import MySQLdb
db=MySQLdb.connect('127.0.0.1','root','','rig')
cursor=db.cursor()
page=urllib2.urlopen("http://www.imd.gov.in/main_new.htm")
data=page.read()
data =data.split('<map name="NotNamed">',1)
data=data[1].split('</map>',1)
data=data[0]
ele=re.findall('<area',data)
link=[]
name=[]
sql="TRUNCATE TABLE `weather`"
cursor.execute(sql)

sql="TRUNCATE TABLE `weatherforecast`"
cursor.execute(sql)

db.commit()
for el in ele:
    url=data.split('href="',1)
    url=url[1].split('alt',1)
    url[0]=url[0].replace('"','')
    url[0]=url[0].strip()
    link.append(url[0])
    city=url[1].split('title="',1)
    city=city[1].split('"',1)
    name.append(city[0])
    data=city[1]


i=0
for li in link:
    try:
        city=name[i]
        today=datetime.date.today()
        print li
        page1=urllib2.urlopen(li)
        data1=page1.read().lower()
        foreContent=data1.split("today's forecast")
        after=foreContent[1].split('<font size="1+">',1)
        forecast = after[1].split('</font>',1)[0].strip()
        
        i=i+1
        val=[]
        for j in range(9):
            ti=data1.split('<font size="1+">',1)
            ti=ti[1].split('(',1)
            res=ti[1].split('<font size="1+">',1)
            res=res[1].split('</font>',1)
            res[0]=res[0].strip()
            data1=res[1]
            val.append(res[0])
        data1=data1.split('</tr>',1)
        data1=data1[1]

        sql = "INSERT INTO `weather`(`City`,`Maximum`,`Minimum`,`Rainfall`,`Today_Sunset`,`Tomorrow_Sunrise`,`Moonset`,`Moonrise`,`forecast`) values %s "%(str((city,val[0],val[2],val[4],val[5],val[6],val[7],val[8],forecast)))
        cursor.execute(sql)
        db.commit()
        
        fcast=[]
        maxt=[]
        mint=[]

        main=[]
        for k in range(6):

            date1=datetime.date.today() + datetime.timedelta(days=k+1)
            date=data1.split('<font color="#ff0000" size="1+">',1)
            date=date[1].split('</font>',1)
            date[0]=date[0].strip()

            mini=date[1].split('<font color="#0000ff" size="1+">',1)
            mini=mini[1].split('</font>',1)
            mini[0]=mini[0].strip()

            mint.append(mini[0])
            maxi=mini[1].split('<font color="#ff0000" size="1+">',1)
            maxi=maxi[1].split('</font>',1)
            maxi[0]=maxi[0].strip()
            
            maxt.append(maxi[0])
            fore=maxi[1].split('<font color="#000000" size="1+">',1)
            fore=fore[1].split('</font>',1)
            fore[0]=fore[0].strip()
            

            fcast.append(fore[0])
            data1=fore[1]
            main.append((city,k+1,mini[0],maxi[0],fore[0]))
            
        for val in main:

            sql="INSERT INTO weatherforecast(`city`,`time`,`minimum`,`maximum`,`forecast`) VALUES %s" %str(val)
            cursor.execute(sql)
            db.commit()
        
                
                     
            
    except Exception as x:
        print x

db.close()        
    
