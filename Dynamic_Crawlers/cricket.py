import re
import urllib2

from bs4 import BeautifulSoup
from multiprocessing import Pool
page=urllib2.urlopen("http://static.espncricinfo.com/rss/livescores.xml")
data=page.read()
#pool=Pool(processes=6)
dat=re.findall('<guid>(.*)</guid>',data)
des=re.findall("<title>(.*)</title>",data)
des.pop(0)

def gettitle(d,teams):
    import MySQLdb
    import urllib2
    import connection
    db =connection.con()
    cursor=db.cursor()
    page=urllib2.urlopen(d)
    cont=page.read()
    
    soup = BeautifulSoup(cont)
    content=str(soup.title.string)
    desc = soup.find('meta',{'name':'description'}).attrs['content']
    desc=str(desc).replace('&amp;','&')
#    print desc
    print "teams "+teams
    if '(' in str(content):
        score=str(content).split('(',1)
        score1=score[0].split('>',1)
        print score1[0]
        score=score[1].split(')',1)
        status=['']
        try:
            status=cont.split('<div class="innings-requirement">',1)
            status=status[1].split('</div>',1)
        except:
            pass
        status=status[0].strip()
        score=score[0].split(',')
        bat=[]
        bowl=''
        for s in score:
            if '/' in s:
      #          print "bowling : "+str(s)
                bowl=str(s)
            else:
       #         print "batting : "+str(s)
                bat.append(str(s))
        num=d.split('/')
       # print len(num)
        num=num[len(num)-1]
      #  print num
        cursor.execute("SELECT * FROM cricket WHERE matchno='%s'"%str(num).replace('.html',''))
        check=cursor.fetchall()
        if check:
       #     print "entered"
        #    print score1[0].split()[0]
         #   print check[0][4]
          #  print bat
	    print desc
            if (score1[0].split()[0] in check[0][4]) and len(bat)==3:
            
                cursor.execute("UPDATE cricket SET score='%s',teams='%s',overs='%s',bat1='%s',bat2='%s',bowl='%s',status='%s',description='%s' WHERE matchno='%s'"%(score1[0].strip(),teams,bat[0],bat[1],bat[2],bowl,status,desc,str(num).replace('.html',''))) 

		db.commit()
                print "updated"
            elif (score1[0].split()[0] not in check[0][4]) and len(bat)==3:
                cursor.execute("UPDATE cricket SET score='%s',score1='%s',teams='%s',overs='%s',bat1='%s',bat2='%s',bowl='%s',status='%s',description='%s' WHERE matchno='%s'"%(score1[0].strip(),check[0][4],teams,bat[0],bat[1],bat[2],bowl,status,desc,str(num).replace('.html','')))
		db.commit()
                print "updated1"
            elif (score1[0].split()[0] in check[0][4]) and len(bat)==2:
                cursor.execute("UPDATE cricket SET score='%s',teams='%s',overs='%s',bat1='%s',bowl='%s',status='%s',description='%s' WHERE matchno='%s'"%(score1[0].strip(),teams,bat[0],bat[1],bowl,status,desc,str(num).replace('.html',''))) 
		db.commit()
                print "updated2"
            elif (score1[0].split()[0] not in check[0][4]) and len(bat)==2:
                cursor.execute("UPDATE cricket SET score='%s',score1='%s',teams='%s',overs='%s',bat1='%s',bowl='%s',status='%s',description='%s' WHERE matchno='%s'"%(score1[0].strip(),check[0][4],teams,bat[0],bat[1],bowl,status,str(num).replace('.html',''),desc))
		db.commit()
                print "updated3"
           # db.commit()
        else:                       


            if len(bat)==3:
                cursor.execute("INSERT INTO cricket (teams,score,overs,bat1,bat2,bowl,matchno,status,description) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(teams.replace('&amp;','&'),score1[0],bat[0],bat[1],bat[2],bowl,str(num).replace('.html',''),status,desc))

                db.commit()
            elif len(bat)==2:
                cursor.execute("INSERT INTO cricket (teams,score,overs,bat1,bowl,matchno,status,description) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(teams.replace('&amp;','&'),score1[0],bat[0],bat[1],bowl,str(num).replace('.html',''),status,desc))

                db.commit()



i=0
print des
for d in dat:
    try:
        
        print "hhjk"
        gettitle(d,des[i].replace('&amp;','and'))
        i=i+1
        
    except Exception as x:
        print x
        i=i+1

    
    
