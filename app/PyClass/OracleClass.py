import cx_Oracle
import os
import pandas as pd
from app.PyClass import XMLClass as XML

xml = XML.XMLclass('dataSource')

#os.environ["NLS_LANG"] = ".AL32UTF8"
#os.putenv('NLS_LANG','KOREAN_KOREA.KO16MSWIN949')
os.putenv('NLS_LANG','AMERICAN_AMERICA.AL32UTF8')


class Oracle():
    def __init__(self,connectName='oracle'):

        conString = xml.getData(f"{connectName}.user") + "/" + xml.getData(f"{connectName}.password") + "@" \
                    + xml.getData(f"{connectName}.host") + "/" + xml.getData(f"{connectName}.sid")


        try:
            self.con = cx_Oracle.connect(conString)
           # print("Oracle version:", self.con.version)
        except cx_Oracle.Error as e:
            print(f"oracle __init__ Error: {e}")

    def getCon(self):
        return self.con

    def close(self):
        try:
            self.con.close()
        except cx_Oracle.Error as e:
            print(f"oracle close Error: {e}")

    def select(self, query,params=None):
        try:
            cur = self.con.cursor()
            if params != None:
                cur.execute(query,params)
            else:
                cur.execute(query)
        except cx_Oracle.Error as e:
            print(f"oracle getCursor Error: {e}")
        return cur

    def selectPandasDataFrame(self, query, params=None):
        try:
            if params != None:
                df = pd.read_sql(sql=query, params=params, con=self.con)
            else:
                df = pd.read_sql(sql=query, con=self.con)

        except cx_Oracle.Error as e:
            print(f"oracle selectPandasDataFrame Error: {e}")
        return df

    def getResultToDataFrame(self, query, params=None):
        try:
            if params != None:
                df = pd.read_sql(sql=query, params=params, con=self.con)
            else:
                df = pd.read_sql(sql=query, con=self.con)

        except cx_Oracle.Error as e:
            print(f"oracle selectPandasDataFrame Error: {e}")
        return df

    def insert(self,query,bindval):
        try:
            cur = self.con.cursor()
            cur.execute(query,bindval)
        except cx_Oracle.Error as e:
            print(f"oracle insert Error: {e}")
        return cur


    def insertmany(self,query,bindval):
        cur = self.con.cursor()
        cur.executemany(query,bindval)

    def update(self,query,bindval):
        try:
            cur = self.con.cursor()
            cur.execute(query,bindval)
        except cx_Oracle.Error as e:
            print(f"oracle update Error: {e}")
        return cur

    def query(self,query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
            #print(query)
        except cx_Oracle.Error as e:
            print(f"oracle query Error: {e}")
        return cur

    def callproc(self,procNm  ):
        try:
            cur = self.con.cursor()


            cur.callproc(procNm)

        except cx_Oracle.Error as e:
            print(f"oracle callproc Error: {e}")
            return 0
        return 1



    def commit(self):
        try:
            self.con.commit()
        except cx_Oracle.Error as e:
            print(f"commit Error: {e}")



