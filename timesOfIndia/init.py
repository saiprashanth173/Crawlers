import MySQLdb,sys,config,months
db = MySQLdb.connect(config.host,config.user,config.passwd)
cursor = db.cursor()
import json
try:
    cursor.execute("CREATE DATABASE %s"%(str(config.db)))
    db.commit()
except Exception as x:
    print x
db.select_db(config.db)
fil = open("track_file","w")
temp= {}
def getStart(year,month,date):
    start= 36892+int(date)-1
    year = int(year)
    month = int(month)
    date= int(date)
    for i in range(2001,int(year)):
        if i%4==0 and year!=2001:
            start+=366
        elif year!=2001:
            start+=365
    for i in range(1,int(month)):
        start+=months.months[str(i)]
    if int(month)>2 and year%4==0:
        start+=1
    return start
        
        
            
if len(sys.argv)==1:
    temp = {"year":2001,"month":1,"day":1,"start":36892}
elif len(sys.argv==2):
    temp = {"year":sys.argv[1],"month":1,"day":1,"start":getStart(sys.argv[1],1,1)}
elif len(sys.argv==3):
    temp = {"year":sys.argv[1],"month":sys.argv[2],"day":1,"start":getStart(sys.argv[1],sys.argv[2],1)}
elif len(sys.argv==4):
    temp = {"year":sys.argv[1],"month":sys.argv[2],"day":sys.argv[3],"start":getStart(sys.argv[1],sys.argv[2],sys.argv[3])}
fil.write(json.dumps(temp))
fil.close()

cursor.execute("CREATE TABLE IF NOT EXISTS page_content(`id` int AUTO_INCREMENT PRIMARY KEY,`url` VARCHAR(200) UNIQUE KEY,`meta_description` VARCHAR(800),`title` VARCHAR(300), `body` VARCHAR(3000),`tstamp` VARCHAR(80) ) ")
db.commit()
