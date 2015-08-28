import MySQLdb

def getContent():
    db = MySQLdb.connect('127.0.0.1','root','root','google_plus')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT name FROM names_single WHERE status!='done' order by `name` desc limit 0,600"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def startOperation(name):
    print name
    db = MySQLdb.connect('127.0.0.1','root','root','google_plus')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    import get_profiles
    get_profiles.getAllProfiles(name)
    try:
        sql = "update names_single SET status = 'done' where `name`='%s'"%(name)
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x
    db.close()


def main():
    import threading
    data = getContent()
    while data:
        
        for dat in data:
            startOperation(dat["name"])
        #break

    data = getContent()
            
            
main()
