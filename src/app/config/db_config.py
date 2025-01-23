import mysql.connector
from mysql.connector import Error
from config.config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_PORT

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def create_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DATABASE,
                    port=MYSQL_PORT
                )
                if self.connection.is_connected():
                    print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")
        return self.connection