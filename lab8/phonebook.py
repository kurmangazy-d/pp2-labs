from connect import connect


def search_contacts():
    pattern = input("Enter search pattern: ")
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def add_contact():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s, %s)", (name, surname, phone))
    conn.commit()

    cur.close()
    conn.close()


def bulk_insert():
    names = input("Enter names (comma): ").split(",")
    surnames = input("Enter surnames (comma): ").split(",")
    phones = input("Enter phones (comma): ").split(",")

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM insert_many_contacts(%s, %s, %s)",
        (names, surnames, phones)
    )

    invalid = cur.fetchall()

    if invalid:
        print("Invalid data:")
        for row in invalid:
            print(row)
    else:
        print("All contacts inserted successfully")

    conn.commit()
    cur.close()
    conn.close()


def delete_contact():
    name = input("Enter name (or leave empty): ")
    phone = input("Enter phone (or leave empty): ")

    name = name if name else None
    phone = phone if phone else None

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s, %s)", (name, phone))
    conn.commit()

    cur.close()
    conn.close()


def paginate_contacts():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Search")
        print("2. Add/Update contact")
        print("3. Delete contact")
        print("4. Show with pagination")
        print("5. Bulk insert")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            paginate_contacts()
        elif choice == "5":
            bulk_insert()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()