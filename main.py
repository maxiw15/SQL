import psycopg2


def create_db(cur):
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


def add_client(cur, first_name, last_name, email, phones=None):
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


def add_phone(cur, client_id, phone):
    cur.execute("""
            INSERT INTO telephone(telephone_id, number) 
            VALUES(%s, %s);""", (client_id, phone))


def find_client(cur, first_name='%', last_name='%', email='%', phone='%'):
    cur.execute("""SELECT c.id, name, surname, email, number FROM client c JOIN telephone t ON 
    c.id=t.telephone_id WHERE (name LIKE %s) and (surname LIKE %s) and (email LIKE %s) and (number LIKE %s);""",
                (first_name, last_name, email, phone))
    found = cur.fetchall()
    print(found)
    return found


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""SELECT c.id, name, surname, email, number FROM client c JOIN telephone t ON 
    c.id=t.telephone_id WHERE c.id = %s;""", (int(client_id),))
    telephone = []
    found = cur.fetchall()
    for i in found:
        name = i[1]
        surname = i[2]
        mail = i[3]
        telephone.append(i[4])
    if first_name is not None:
        name = first_name
    if last_name is not None:
        surname = last_name
    if email is not None:
        mail = email
    if phones is not None:
        print("Напишите порядковый номер телефона, который вы хотите изменить")
        print(telephone)
        i = int(input())
        cur.execute("""
        UPDATE telephone SET number=%s WHERE number LIKE %s;""", (phones, telephone[i-1]))

    cur.execute("""
    UPDATE client SET name=%s, surname=%s, email=%s WHERE id=%s;""", (name, surname, mail, client_id))


def delete_phone(cur, client_id, phone):
    cur.execute("""
               DELETE FROM telephone
               WHERE telephone_id=%s and number=%s;""", (client_id, phone))


def delete_client(cur, client_id):
    cur.execute("""
            DELETE FROM telephone
            WHERE telephone_id =%s;""", client_id)

    cur.execute("""
    DELETE FROM client
    WHERE id =%s;""", client_id)


def delete_db(cur):
    cur.execute("""
    DROP TABLE telephone CASCADE;
    DROP TABLE client CASCADE;
    """)


if __name__ == "__main__":
    with psycopg2.connect(database="testdb2", user="testuser", password="123456", host="localhost") as connect:
        with connect.cursor() as cur:
            delete_db(cur)
            create_db(cur)
            add_client(cur, "Max", "Ivanov", "max.iw15@yandex.ru", "8491233123")
            add_phone(cur, '1', '9123121233')
            add_phone(cur, '1', '912312433')
            add_phone(cur, '1', '4212311233')
            # delete_phone(cur, '1', '912312433')
            # delete_client(cur, '1')
            # change_client(cur, client_id='1', last_name='Max', first_name="Ivanov",email="max.iw", phones='12314f')
            find_client(cur, last_name='Ivanov')
            change_client(cur, client_id='1', last_name='Ivanov', phones="234234234")
            find_client(cur, first_name='Max')
    connect.close()
