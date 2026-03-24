import psycopg2
from config import load_config

def querying_1():
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, first_name FROM phonebook ORDER BY first_name")
                print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def querying_2():
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, phone FROM phonebook ORDER BY phone")
                print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    querying_1()
    querying_2()