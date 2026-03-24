import psycopg2
import csv
from config import load_config


def insert_np(name,phone):
    sql = """INSERT INTO phonebook(first_name,phone)
             VALUES(%s, %s) RETURNING id;"""
    
    id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name,phone))
                row = cur.fetchone()
                if row:
                    id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return id

def insert_from_csv(filename):
    sql = """INSERT INTO phonebook(first_name, phone)
             VALUES (%s, %s);"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        first_name, phone = row
                        cur.execute(sql, (first_name, phone))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

name = input()
phone = input()

if __name__ == '__main__':
    insert_np(name,phone)
    insert_from_csv('filename.csv')

