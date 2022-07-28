import psycopg2

# Функция удаления таблиц
def drop_tables(cursor):
    cur.execute("""
        DROP TABLE clients
        CASCADE;
        DROP TABLE phone_numbers
        CASCADE;
        """)
    return conn.commit()

# Функция, создающая структуру БД (таблицы)
def create_tables(cursor):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(40) NOT NULL,
                    email VARCHAR(40) UNIQUE NOT NULL
                );
                """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_numbers(
                id SERIAL PRIMARY KEY,
                phonenumber varchar(50) NOT NULL,
                client_id INTEGER NOT NULL REFERENCES clients(id)
            );
            """)
    return conn.commit()

# Функция, позволяющая добавить нового клиента
def add_client(conn, id, name, surname, email, phonenumber=None):
    cur.execute("""
           INSERT INTO clients (id, name, surname, email) 
           VALUES (%s, %s, %s, %s) ;
           """, (id, name, surname, email))
    conn.commit()
    cur.execute("""
           INSERT INTO phone_numbers (client_id, phonenumber) 
           VALUES (%s, %s) RETURNING id;
           """, (id, phonenumber))
    print(cur.fetchone())

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phonenumber):
    cur.execute("""
           INSERT INTO phone_numbers (client_id, phonenumber) 
           VALUES (%s, %s) RETURNING id;
           """, (client_id, phonenumber))
    print(cur.fetchone())

# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, name=None, surname=None, email=None, phonenumber=None):
    cur.execute("""
                UPDATE clients SET name=%s, surname=%s, email=%s  WHERE id=%s;
                """, (name, surname, email, client_id))
    cur.execute("""
                SELECT * FROM clients;
                """)
    conn.commit()

    cur.execute("""
                UPDATE phone_numbers SET phonenumber=%s WHERE id=%s;
                """, (phonenumber, client_id))
    cur.execute("""
                SELECT * FROM phone_numbers;
                """)
    print(cur.fetchone())

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id):
    cur.execute("""
            DELETE FROM phone_numbers WHERE id=%s;
            """, (client_id,))
    cur.execute("""
            SELECT phonenumber FROM phone_numbers;
            """)
    print(cur.fetchall())

# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    cur.execute("""
            DELETE FROM phone_numbers  WHERE client_id=%s;
            """, (client_id,))
    cur.execute("""
            SELECT * FROM phone_numbers ;
            """)
    cur.execute("""
            DELETE FROM clients  WHERE id=%s;
            """, (client_id,))
    cur.execute("""
            SELECT * FROM clients ;
            """)
    print(cur.fetchall())

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(conn, name=None, surname=None, email=None, phonenumber=None):
    cur.execute("""
                SELECT id FROM clients WHERE name=%s or surname=%s or email=%s;
                """, (name, surname, email))
    cur.execute("""
                SELECT client_id FROM phone_numbers WHERE phonenumber=%s;
                """, (phonenumber,))
    print(cur.fetchall())

if __name__ == "__main__":
    with psycopg2.connect(database="HW_5", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            drop_tables(conn)
            create_tables(conn)
            add_client(conn, '1', 'Andrey', 'Ivanov', 'ivanov@mail.ru', '888-888-88-88')
            add_client(conn, '2', 'Oleg', 'Petrov', 'petrov@mail.ru', '222-222-22-22')
            add_client(conn, '3',  'Igor', 'Sidorov', 'sidorov@mail.ru', '777-777-77-77')
            add_phone(conn, 1, '999-999-99-99')
            add_phone(conn, 1, '555-555-55-55')
            add_phone(conn, 2, '111-111-11-11')
            add_phone(conn, 3, '333-333-33-33')
            change_client (conn, 1, name = 'Kirill', surname = 'No', email = 'no@mail.ru', phonenumber='000-000-00-00')
            delete_phone(conn, 1)
            delete_client(conn, 2)
            find_client(conn, name = '*', surname = 'No', email = '*', phonenumber='555-555-55-55')
    conn.close()
