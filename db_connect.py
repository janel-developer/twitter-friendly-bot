import psycopg2
import os

DBUSER = os.getenv("DBUSER")
DBPW = os.getenv("DBPW")
DBNAME = os.getenv("TWITTERDB")


def connect_to_db(username=DBUSER, pw=DBPW, dbname=DBNAME):
    try:
        connection = 0
        connection = psycopg2.connect(user=username,
                                      password=pw,
                                      host="127.0.0.1",
                                      port="5432",
                                      database=dbname)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        if record:
            print("You are connected to database\n")
            cursor.execute(
                """SELECT table_name FROM  information_schema.tables WHERE table_schema = 'public'""")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        # closing database connection.
        close_db(connection)
    return connection


def close_db(connection):
    # closing database connection.
    if(connection):
        connection.cursor().close()
        connection.close()
        print("Database connection is closed\n")
