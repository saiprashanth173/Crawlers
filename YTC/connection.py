import pymysql
dbFirst = pymysql.connect('127.0.0.1','root','#srmseONserver1')
try:
    db = pymysql.connect('127.0.0.1','root','#srmseONserver1','yt')
except:
    
    pass

