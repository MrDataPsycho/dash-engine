import csv
import sqlite3
from sqlite3 import Error


def read_stock_data():
    with open("instances/stockdata.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        data = [tuple(row) for row in reader]
    return data


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(db, create_table_sql):
    """ create a table from the create_table_sql statement
    :param db: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def inset_data_stock(db: str, name: str, data_list: list):
    """
     Create a new project into the projects table
     :param db: connection
     :param name: table name
     :param data_list: list of data
     :return: name: id
     """
    drop_sql = '''DELETE FROM {};'''.format(name)
    insert_sql = '''
        INSERT INTO {}(stock_date, stock, value, change)
        VALUES(?, ?, ?, ?);
    '''.format(name)
    conn = sqlite3.connect(db)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute(drop_sql)
            for item in data_list:
                cur.execute(insert_sql, item)
        return print("Data Inserted")
    except Error as e:
        print(e)


# Creating Database and Tables

stock_data = read_stock_data()

table_def_stock = """
    CREATE TABLE IF NOT EXISTS daily_stock (
        stock_date TEXT NOT NULL,
        stock TEXT NOT NULL,
        value FLOAT NOT NULL,
        change FLOAT NOT NULL
);
"""

# =========
# Data IO
# =========
db_path = "instances/sample.db"
create_connection(db_path)
create_table(db_path, table_def_stock)
inset_data_stock(db_path, "daily_stock", stock_data)


