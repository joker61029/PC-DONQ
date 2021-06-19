import mysql.connector, json
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()
mydb = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_user'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_DATABASE')
)
cursor = mydb.cursor(buffered=True)
sql ="""
    CREATE TABLE message(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    text varchar(255) NOT NULL,
    image varchar(255),
    PRIMARY KEY (id));
    """
cursor.execute(sql)