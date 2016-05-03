import MySQLdb
import os

def connection():
    ''' creates connection with local/remote database '''
    conn = MySQLdb.connect (host = os.environ["HOST"],
                            port = int(os.environ["PORT"]),
                            user = os.environ["DBUSER"],
                            passwd = os.environ["DBPASSWD"],
                            db = os.environ["DB"])
    c = conn.cursor()

    return c, conn
