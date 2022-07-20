import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_tables(cursor):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE clients
        CASCADE;
        DROP TABLE phone_numbers
        CASCADE;
        """)
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
def add_client(conn, name, surname, email, phonenumber=None):
    with conn.cursor() as cur:
        cur.execute("""
               INSERT INTO clients (name, surname, email) 
               VALUES (%s, %s, %s) RETURNING id;
               """, (name, surname, email))
        print(cur.fetchone())

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phonenumber):
    with conn.cursor() as cur:
        cur.execute("""
               INSERT INTO phone_numbers (client_id, phonenumber) 
               VALUES (%s, %s) RETURNING id;
               """, (client_id, phonenumber))
        print(cur.fetchone())

# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                    UPDATE clients SET name=%s WHERE id=%s;
                    """, (name, client_id))
        cur.execute("""
                    SELECT * FROM clients;
                    """)
        print(cur.fetchone())

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id, phonenumber):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phone_numbers WHERE id=%s;
                """, (client_id,))
        cur.execute("""
                SELECT phonenumber FROM phone_numbers;
                """)
        print(cur.fetchall())

# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
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
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id FROM clients WHERE name=%s;
                    """, (name,))
        print(cur.fetchall())

with psycopg2.connect(database="HW_5", user="postgres", password="postgres") as conn:
    create_tables(conn)
    add_client(conn, 'Andrey', 'Ivanov', 'ivanov@mail.ru')
    add_client(conn, 'Oleg', 'Petrov', 'petrov@mail.ru')
    add_client(conn, 'Igor', 'Sidorov', 'sidorov@mail.ru')
    add_phone(conn, 1, '999-999-99-99')
    add_phone(conn, 1, '555-555-55-55')
    add_phone(conn, 2, '111-111-11-11')
    add_phone(conn, 3, '333-333-33-33')
    change_client (conn, 1, 'Kirill')
    delete_phone(conn, 1, '999-999-99-99')
    delete_client(conn,2)
    find_client(conn, 'Igor')
conn.close()
