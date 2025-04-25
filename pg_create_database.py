import psycopg2 as pg
from psycopg2 import sql
from db_settings import config


DATABASE_NAME = config.DATABASE_NAME
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD

conn = pg.connect(
    dbname="postgres", user=DB_USER, password=DB_PASSWORD, host="localhost", port="5432"
)

conn.autocommit = True  # Включаем автокоммит, иначе CREATE DATABASE не сработает


try:
    # Создаем курсор и выполняем SQL-запрос
    with conn.cursor() as cur:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
        # cur.execute("CREATE DATABASE test_db")
        print(f"База данних '{DATABASE_NAME}' створена!")

except pg.Error as e:
    print("Error connecting or creating database:", e)

finally:
    if conn:
        conn.close()
        