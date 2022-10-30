from venv import create
import psycopg2


hostname = 'localhost'
database = 'switchDatabase'
username = 'postgres'
pwd = 'Hello There!'
port_id = 5432
connection = None

query = ""
#Reset table if needed
def createTable():
    try:
        with psycopg2.connect(
                        host = hostname,
                        dbname = database,
                        user = username, 
                        password = pwd,
                        port = port_id
        ) as connection:
            with connection.cursor() as cursor:
                query = """
                DROP TABLE IF EXISTS SWITCH"""
                cursor.execute(query)
                create_table = """CREATE TABLE SWITCH(
                    id      serial PRIMARY KEY,
                    owner   varchar(40) NOT NULL,
                    name    varchar(50) NOT NULL,
                    type    varchar(10),
                    links   JSONB
                )
                
                """
                
                cursor.execute(create_table)
    
    except Exception as error:
        print(error)
        
    finally:
        if connection != None:
            connection.close()


#Connection to database
def connect():
    try:
        connection = psycopg2.connect(
                        host = hostname,
                        dbname = database,
                        user = username, 
                        password = pwd,
                        port = port_id
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as error:
        print(error)