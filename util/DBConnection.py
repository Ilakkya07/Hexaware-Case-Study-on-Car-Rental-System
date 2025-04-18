import pyodbc
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.PropertyUtil import DBPropertyUtil 
class DBConnUtil:
    @staticmethod
    def getConnection():
        conn_str=DBPropertyUtil.getPropertyString('resources/db.properties')
        print(f"Connection String: {conn_str}")
        try:
            conn=pyodbc.connect(conn_str)
            print("Connection established successfully.")
            return conn
        except pyodbc.Error as e:
            print(f"Connection failed: {e}")
            return None


