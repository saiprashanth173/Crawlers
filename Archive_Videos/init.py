
import MySQLdb
import config
db = MySQLdb.connect(config.host,config.user,config.paswd)
cursor = db.cursor()

try :
    cursor.execute("CREATE DATABASE "+config.db)
    db.commit()
    db.select_db(config.db)

except Exception as x:
    print x


# create required tables 
try:
    cursor.execute("CREATE TABLE IF NOT EXISTS archive_collections(`id` INT AUTO_INCREMENT, `link` VARCHAR(400) UNIQUE KEY, `status` VARCHAR(30)) ENGINE = MYISAM")
    cursor.execute("CREATE TABLE IF NOT EXISTS archive_videos(`id` INT AUTO_INCREMENT, `link` VARCHAR(400) UNIQUE KEY, `views` VARCHAR(30),`fav` VARCHAR(20), `img` VARCHAR(100) ) ENGINE = MYISAM")
    db.commit()
    
except Exception as x:
    print x

    
    

