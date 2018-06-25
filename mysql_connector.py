import MySQLdb


class DbConnector:

    def __init__(self, host, username, password, db):
        self.db = MySQLdb.connect(host, username, password, db)
        self.cursor = self.db.cursor()

    def get_version(self):

        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        return data

    def write(self, host, ip, site, load_time, nav_time):
        sql = "INSERT INTO qa_delhi(HOSTNAME, IP, SITE, LOAD_TIME, NAV_TIME) VALUES('%s',%s,%s,%s,%s)" % (host, ip, site, load_time, nav_time)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def db_close(self):
        self.db.close()

