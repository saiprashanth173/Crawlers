
import MySQLdb
import config
db = MySQLdb.connect(config.host,config.user,config.paswd)
cursor = db.cursor()

try :
    cursor.execute("CREATE DATABASE "+config.db)
    db.commit()
    
except Exception as x:
    print x


# create required tables 
try:
    db.select_db(config.db)

    cursor.execute("CREATE TABLE IF NOT EXISTS archive_collections(`id` INT AUTO_INCREMENT PRIMARY KEY, `link` VARCHAR(400) UNIQUE KEY,`present_link` int, `status` VARCHAR(30) DEFAULT '') ENGINE = MYISAM")
    cursor.execute("CREATE TABLE IF NOT EXISTS archive_videos(`id` INT AUTO_INCREMENT PRIMARY KEY, `link` VARCHAR(400) UNIQUE KEY,`title` VARCHAR(200), `views` VARCHAR(30),`fav` VARCHAR(20), `img` VARCHAR(100) ) ENGINE = MYISAM")
    cursor.execute("INSERT INTO archive_collections(`link`,`present_link`) VALUES ('https://archive.org/details/movies?&sort=-downloads&page=','1')")
    db.commit()
    
    
except Exception as x:
    print x


    
    

