import MySQLdb
db = MySQLdb.connect('127.0.0.1','root','root')
cursor = db.cursor()
from bs4 import BeautifulSoup as bs
try:
    cursor.execute('Create database dailymotion')
except Exception as x:
    pass


db.select_db('dailymotion')

try:
    cursor.execute("CREATE TABLE IF NOT EXISTS channels (id INT AUTO_INCREMENT PRIMARY KEY,channel_name VARCHAR(30) ,channel_link VARCHAR(500) UNIQUE KEY,crawled INT DEFAULT 0) ")
    db.commit()
except Exception as x:
    print "Channels table already exists"

try:

    cursor.execute("CREATE TABLE IF NOT EXISTS main_links (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500),description VARCHAR(500), link VARCHAR(500) UNIQUE KEY,img_link VARCHAR(500),duration VARCHAR(30), duration_changed VARCHAR(100), channel_name VARCHAR(100))")
    cursor.execute("CREATE TABLE IF NOT EXISTS track_table (channel_link VARCHAR(500) PRIMARY KEY,next_link VARCHAR(500), next_link_nc VARCHAR(500), status int, channel_name varchar(60) UNIQUE KEY)")
    db.commit()
except Exception as x:
    print (x)

    
# used for geting the page source
def getPageSource(url):
    import urllib2
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(req)
    source = page.read()
    source = source.decode('unicode_escape').encode('ascii','ignore')
    return bs(source)
