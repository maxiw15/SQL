import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(40) NOT NULL,
                    email VARCHAR(20) 
                    
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS telephone(
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(11) UNIQUE,
                    telephone_id INTEGER NOT NULL REFERENCES client(id)
                );
                """)

        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, surname, email) 
        VALUES(%s, %s, %s);""", (first_name, last_name, email))

        cur.execute("""
        SELECT CURRVAL(pg_get_serial_sequence('client', 'id'));
        """)

        telephone_id = cur.fetchone()

        cur.execute("""
               INSERT INTO telephone(telephone_id, number) 
               VALUES(%s, %s);""", (telephone_id, phones))

        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
               INSERT INTO telephone(telephone_id, number) 
               VALUES(%s, %s);""", (client_id, phone))

        conn.commit()


def find_client(conn, first_name='%', last_name='%', email='%', phone='%'):
    with conn.cursor() as cur:
        cur.execute("""SELECT c.id, name, surname, email, number FROM client c JOIN telephone t ON 
        c.id=t.telephone_id WHERE (name LIKE %s) and (surname LIKE %s) and (email LIKE %s) and (number LIKE %s);""",
                    (first_name, last_name, email, phone))
        found = cur.fetchall()
        print(found)
        return found


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:

        cur.execute("""
        UPDATE client SET name=%s, surname=%s, email=%s WHERE id=%s;""", (first_name, last_name, email, client_id))

        cur.execute("""
               DELETE FROM telephone
               WHERE telephone_id =%s;""", client_id)
        conn.commit()
        cur.execute("""
               INSERT INTO telephone(telephone_id, number) 
               VALUES(%s, %s);""", (client_id, phones))

        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
               DELETE FROM telephone
               WHERE telephone_id=%s and number=%s;""", (client_id, phone))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
               DELETE FROM telephone
               WHERE telephone_id =%s;""", client_id)

        cur.execute("""
        DELETE FROM client
        WHERE id =%s;""", client_id)

        conn.commit()


def delete_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE telephone CASCADE;
        DROP TABLE client CASCADE;
        """)


with psycopg2.connect(database="testdb2", user="testuser", password="123456", host="localhost") as connect:
    # delete_db(connect)
    # create_db(connect)
    # add_client(connect, "Max", "Ivanov", "max.iw15@yandex.ru", "8491233123")
    # add_phone(connect, '1', '9123121233')
    # add_phone(connect, '1', '912312433')
    # add_phone(connect, '1', '4212311233')
    # delete_phone(connect, '1', '912312433')
    # delete_client(connect, '1')
    # change_client(connect, client_id='1', last_name='Max', first_name="Ivanov",email="max.iw", phones='12314f')
    find_client(connect, 'Ivanov')
connect.close()
