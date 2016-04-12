import MySQLdb

def connection():
    ''' creates connection with local/remote database '''
    conn = MySQLdb.connect (host = "orders.cn9rvzzvqepf.us-west-2.rds.amazonaws.com",
                            port = 3306,
                            user = "nyutircaterpi",
                            passwd = "cAterPI2016",
                            db = "orders")
    c = conn.cursor()

    return c, conn
