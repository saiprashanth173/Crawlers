import urllib2

from bs4 import BeautifulSoup as bs
import connection
db = connection.db
cursor = db.cursor()


# used for getting the required links
def getContent(soup):

    requiredDiv = soup.find('div',{'class':'row'})
    links = requiredDiv.findAll('a',{'class':'link'})
    for link in links:
        try:
            
            url = "http://www.dailymotion.com/user/"+link.attrs['href'].split("/")[-1]
            name = link.text
            print name
            

            
            storeURL(name.strip(),url)
        except Exception as x:
            print x

#stores url in the required table 
def storeURL(name,url):
    try:
        
        cursor.execute("INSERT INTO channels(`channel_name`,`channel_link`) VALUES ('%s','%s')"%(name,url))
        db.commit()
    except Exception as x:
        print x


def main():
    for i in range(1,101):
        soup = connection.getPageSource("http://www.dailymotion.com/users/popular/channel/all/"+str(i))
        getContent(soup)
    

main()
