import configparser

class DBPropertyUtil:
    @staticmethod
    def getPropertyString(filename):
        config=configparser.ConfigParser()
        try:
            config.read(filename)
            section=config['DB']
            host=section['host']
            dbname=section['dbname']
            port=section.get('port', '1433')  
        except KeyError as e:
            print(f"Missing expected property: {e}")
            return None
        except FileNotFoundError:
            print(f"Configuration file {filename} not found.")
            return None
        except Exception as e:
            print(f"Error reading the property file: {e}")
            return None
        print(f"Trying to connect to: {host}, Database: {dbname}, Port: {port}")
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={dbname};Trusted_Connection=yes"
        return conn_str

