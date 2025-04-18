import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.DBConnection import DBConnUtil

def main():
    conn=DBConnUtil.getConnection()
    if conn:
        print("Connection is active.")
        conn.close()
    else:
        print("Connection failed.")

if __name__ == '__main__':
    main()
