import MySQLdb


class DbConnector:

    def __init__(self, username, password, db):
        self.db = MySQLdb.connect("localhost", username, password, db)
        self.cursor = self.db.cursor()

    def get_version(self):

        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        return data

    def write(self, site, req_time, render_time, load_time, nav_time):
        sql = "INSERT INTO test_delhi(SITE, REQ_TIME, PAGE_RENDER_TIME, LOAD_TIME, NAV_TIME) VALUES('%s',%s,%s,%s,%s)" % (site, req_time, render_time, load_time, nav_time)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def db_close(self):
        self.db.close()

