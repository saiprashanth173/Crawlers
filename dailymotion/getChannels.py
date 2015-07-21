import urllib2

from bs4 import BeautifulSoup as bs
import connection
db = connection.db
cursor = db.cursor()


# used for getting the required links
def getContent(soup):

    requiredDiv = soup.find('div',{'class':'explore_wrapper'})
    links = requiredDiv.findAll('a')
    for link in links:
        try:
            url = "http://www.dailymotion.com"+link.attrs['href']
            name = link.text
            

            
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

    soup = connection.getPageSource("http://www.dailymotion.com/in/browse")
    getContent(soup)
    

main()
