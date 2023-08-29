import psycopg2

# Параметри підключення
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword',
    'host': 'localhost',
    'port': 5432
}

conn = psycopg2.connect(**db_params)


cur = conn.cursor()
cur.execute("commit")  
cur.execute("create database mydb")
cur.close()
conn.close()