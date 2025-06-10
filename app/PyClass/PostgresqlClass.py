import psycopg2 as postgresql
from app.PyClass import XMLClass as XML

xml = XML.XMLclass('dataSource')


class Postgresql():
    def __init__(self):
        try:
            # Connect to postgresql Platform
            self.con = postgresql.connect(

                user=xml.getText("postgresql.user"),
                password=xml.getText("postgresql.password"),
                host=xml.getText("postgresql.host"),
                port=xml.getText("postgresql.port"),
                database=xml.getText("postgresql.database")
            )
        except postgresql.Error as e:
            print(f"postgresql __init__ Error: {e}")


    def close(self):
        try:
            self.con.close()
        except postgresql.Error as e:
            print(f"postgresql close Error: {e}")

    def select(self, query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
        except postgresql.Error as e:
            print(f"postgresql getCursor Error: {e}")
        return cur

    def insertmany(self,query,bindval):
            cur = self.con.cursor()
            cur.executemany(query, bindval)

    def update(self,query,bindval):
        try:
            cur = self.con.cursor()
            cur.execute(query,bindval)
        except postgresql.Error as e:
            print(f"postgresql update Error: {e}")
        return cur

    def commit(self):
        try:
            self.con.commit()
       #cur.arraysize = 256
        except postgresql.Error as e:
            print(f"postgresql Error: {e}")

postgre = Postgresql()

p = postgre.select('SELECT version()')
print(p.fetchone())