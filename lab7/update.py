import psycopg2
from config import load_config


def update(id, first_name):
    updated_row_count = 0

    sql = """ UPDATE phonebook
                SET first_name = %s
                WHERE id = %s"""

    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (first_name, id))
                updated_row_count = cur.rowcount
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return updated_row_count

if __name__ == '__main__':
    update(1, "Khalib")