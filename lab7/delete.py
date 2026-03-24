import psycopg2
from config import load_config


def delete_part(id):
    rows_deleted  = 0
    sql = 'DELETE FROM phonebook WHERE id = %s'
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (id,))
                rows_deleted = cur.rowcount
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return rows_deleted

if __name__ == '__main__':
    deleted_rows = delete_part(1)
    print('The number of deleted rows: ', deleted_rows)