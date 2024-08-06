from pymysql import connect, Error
from constants import DB_USERNAME, DB_PASSWORD, DATABASE


class DB:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = connect(
                host="localhost",
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DATABASE
            )
        except Error as e:
            print(e)

    def query(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.conn.commit()
                return result
        except Error as e:
            print(e)

    def close(self):
        self.conn.close()
