import conn
import config
db = conn.db


cursor = db.cursor()

def createRequired():
    try:
        sql = "CREATE DATABASE "+config.db_name
        cursor.execute(sql)
        db.commit()
    except Exception as x:
        print x
    db.select_db(config.db_name)
        
    sql = "CREATE TABLE IF NOT EXISTS user_accounts (`id` int PRIMARY KEY, `type` VARCHAR(100), `display_name` VARCHAR(200),`link` VARCHAR (300), `img` VARCHAR(300), `details_obtained` int, `tag` VARCHAR(200))"
    cursor.execute(sql)
    db.commit()

createRequired()
