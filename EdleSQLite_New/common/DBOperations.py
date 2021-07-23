import sqlite3
from sqlite3 import Error
import os
import config
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
# pip install DBUtils==1.3
from DBUtils.PooledDB import PooledDB

# https://www.programmersought.com/article/78166137449/

LOCALMYSQL = {
        'host':'localhost',
        'user': 'root',
        'password': 'R@ting#2021',#
        'db': 'indexdb',
        'OPTIONS': {
           "init_command": "SET GLOBAL max_connections = 100000"}
}

class DatabaseOp:


    def create_database(self):
        """ create a database connection to a SQLite database """
        DB_FILE = os.getcwd() + '/DB/' + config.DB_Name
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=50)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_mysql_database(self,db_name):
        dataBase = mysql.connector.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'],
                                           password=LOCALMYSQL['password'])
        # preparing a cursor object
        cursorObject = dataBase.cursor()
        # creating database
        query="CREATE DATABASE IF NOT EXISTS "+str(db_name)+";"
        cursorObject.execute(query)
        print("database created")
        return

    def connect2Mysql(self):
        # mysql.connector
        pymysql.threadsafety= 3
        conn = pymysql.connect(host=LOCALMYSQL['host'], user=LOCALMYSQL['user'],password=LOCALMYSQL['password'], database=LOCALMYSQL['db'])
        # pool = PooledDB(pymysql, 10, host=LOCALMYSQL['host'], user=LOCALMYSQL['user'], passwd=LOCALMYSQL['password'], db=LOCALMYSQL['db'], port=3306,
        #                 setsession=['SET AUTOCOMMIT = 1'])  # 5 is the minimum number of connections in the connection pool, setsession=['SET AUTOCOMMIT = 1'] is a configuration to set whether thread pools are turned on for automatic updates, 0 to false, 1 to true
        # conn = pool.connection()
        # pool = PooledDB(MySQLdb, mincached=10, maxcached=10, maxshared=10, maxconnections=10, **connKwargs)
        # return pool
        return conn

    def create_connection(self):
        DB_FILE = os.getcwd() + '/DB/' + config.DB_Name
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE, timeout=50)
            return conn
        except Error as e:
            print(e)

        return conn

    def mdy_to_ymd(selef,date):
        return datetime.strptime(date, '%d%b%y').strftime('%Y-%m-%d')

    # def create_table(self, conn, table_name):
    #     """ create a table from the create_table_sql statement
    #     :param conn: Connection object
    #     :param create_table_sql: a CREATE TABLE statement
    #     :return:
    #     """
    #     # id INTEGER PRIMARY KEY AUTOINCREMENT # this is sqlite statement
    #     # id INTEGER PRIMARY KEY AUTO_INCREMENT # this is sqlite statement
    #     ## old table
    #     # create_table_sql=''' CREATE TABLE IF NOT EXISTS {}(
    #     #                                     id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #     #                                     ScrapedDate TEXT NOT NULL,
    #     #                                     ScripName TEXT NOT NULL,
    #     #                                     IndexORStocks INTEGER NOT NULL,
    #     #                                     StrikePrice TEXT NOT NULL,
    #     #                                     OptionType TEXT NOT NULL,
    #     #                                     StrTradeDateTime TEXT NOT NULL,
    #     #                                     TradeDateTime TEXT NOT NULL,
    #     #                                     ExpiryDate text NOT NULL ,
    #     #                                     OI TEXT NOT NULL,
    #     #                                     COI TEXT NOT NULL,
    #     #                                     IV TEXT NOT NULL,
    #     #                                     VOL TEXT NOT NULL,
    #     #                                     MinuteOI TEXT NOT NULL,
    #     #                                     Flag INTEGER NOT NULL
    #     #                                 );'''.format(table_name)
    #
    #     create_table_sql = ''' CREATE TABLE IF NOT EXISTS {}(
    #                                                 id INTEGER PRIMARY KEY AUTO_INCREMENT,
    #                                                 ScrapedDate date NOT NULL,
    #                                                 ScripName TEXT NOT NULL,
    #                                                 IndexORStocks INTEGER NOT NULL,
    #                                                 StrikePrice float NOT NULL,
    #                                                 OptionType TEXT NOT NULL,
    #                                                 StrTradeDateTime TEXT NOT NULL,
    #                                                 TradeDateTime datetime NOT NULL,
    #                                                 ExpiryDate date NOT NULL ,
    #                                                 OI float NOT NULL,
    #                                                 COI float NOT NULL,
    #                                                 IV float NOT NULL,
    #                                                 VOL float NOT NULL,
    #                                                 MinuteOI TEXT NOT NULL,
    #                                                 Flag INTEGER NOT NULL
    #                                             );'''.format(table_name)
    #     try:
    #         c = conn.cursor()
    #         #print("create_table_sql==",create_table_sql)
    #         c.execute(create_table_sql)
    #         c.close()
    #         #print("Table created successfully")
    #     except Error as e:
    #         print(e)

    def create_tableThreshold(self, conn):
        #InstrumentName, ExpiryDate, Threshold
        ## AUTO_INCREMENT ##MYSQL
        ## AUTOINCREMENT ## SQLITE
        create_table_sql=''' CREATE TABLE IF NOT EXISTS Threshold(
                                            id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                            ScripName TEXT NOT NULL,
                                            ExpiryDate text NOT NULL ,
                                            Threshold TEXT NOT NULL);'''
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            c.close()
            #print("Table created successfully")
        except Error as e:
            print(e)

    def insertThreshold(self, conn, ScripName, ExpiryDate, Threshold):
        #insert_table_sql = """INSERT INTO Threshold (ScripName, ExpiryDate, Threshold) VALUES(?,?,?)"""
        insert_table_sql = """INSERT INTO Threshold (ScripName, ExpiryDate, Threshold) VALUES(%s,%s,%s)"""
        try:
            queryparameter = ScripName, ExpiryDate, Threshold
            c = conn.cursor()
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    def updateThreshold(self, conn, ScripName, ExpiryDate, Threshold):
        #insert_table_sql = """UPDATE Threshold SET Threshold=? WHERE ScripName=? AND ExpiryDate=?"""
        insert_table_sql = "UPDATE Threshold SET Threshold='"+str(Threshold)+"' WHERE ScripName='"+str(ScripName)+"' AND ExpiryDate='"+str(ExpiryDate)+"'"
        try:
            #queryparameter = [Threshold, ScripName, ExpiryDate]
            c = conn.cursor()
            c.execute(insert_table_sql)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    def delete(self, conn):
        create_table_sql = """ delete from stockDetails """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            conn.close()
            print("records deleted successfully")
        except Error as e:
            print(e)


    def checkInsertedRecords(self, conn,DateTime,Symbol,Resolution):
        cur = conn.cursor()
        cur.execute("SELECT id FROM stockDetails WHERE datetime = ? AND symbol= ? AND resolution=?", [DateTime,Symbol,Resolution])
        rows = cur.fetchall()
        return rows

    def insert(self, conn, ScrapedDate, ScripName, IndexORStocks, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime,
               ExpiryDate, OI, COI, IV, VOL, MOI, Flag, table_name):

        ExpiryDate = self.mdy_to_ymd(ExpiryDate)

        # insert_table_sql="""INSERT INTO {} (ScrapedDate, ScripName,IndexORStocks,StrikePrice,OptionType,StrTradeDateTime,
        #                     TradeDateTime,ExpiryDate, OI, COI, IV, VOL, MinuteOI, Flag)
        #                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(table_name)
        insert_table_sql = """INSERT INTO {} (ScrapedDate, ScripName,IndexORStocks,StrikePrice,OptionType,StrTradeDateTime,
                                    TradeDateTime,ExpiryDate, OI, COI, IV, VOL, MinuteOI, Flag)
                                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(table_name)
        try:
            queryparameter = ScrapedDate, ScripName, IndexORStocks, StrikePrice, OptionType, StrTradeDateTime, TradeDateTime, ExpiryDate, OI, COI, IV, VOL, MOI, Flag
            c = conn.cursor()
            c.execute(insert_table_sql, queryparameter)
            conn.commit()
            # print("records inserted successfully")
        except Error as e:
            print(e)

    def DF2SQL(self, data, table_name, engine):
        # engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
        #                        .format(user="root",
        #                                pw="InOut@909",
        #                                db="indexdb"))
        # df = pd.read_sql("select * from {}".format(table_name), engine)
        # final = pd.concat([df, data]).drop_duplicates().reset_index(drop=True)
        # print(final.head())
        # print(final.columns)
        # data['datetime'] = data['datetime'].apply(lambda x: str(x))
        try:
            conn = engine.connect()
            # some simple data operations
            data.to_sql(table_name, con=conn, if_exists='append', chunksize=1000, index=False)
            conn.close()
            # engine.dispose()
        except Exception as e:
            print('Exception in converting DF to SQL:', e)




    # #
    # if __name__ == '__main__':
    #     #### create_database()
    #     conn= create_connection()

        # create_table(conn)
        # dropTable(conn)
        # stockMaster(conn)
        #delete(conn)