import sqlite3
from datetime import datetime as dt

SQL_SELECT = '''SELECT id, name, text, planned, status FROM diary'''

def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d

def initialize(conn): #какой смысл в not null, если можно всё равно скипнуть?
    with conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                text TEXT,
                planned DATETIME NOT NULL,
                status TEXT NOT NULL
            )
        ''')

def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    return conn

def find_id(conn, id):
    with conn: # для чего кроме сохранения нужен with conn? зачем его тут писать?
        cursor = conn.execute(SQL_SELECT + " WHERE id=?", (id,))
        return cursor.fetchone()

def print_all(conn):
    date = dt.now().date()
    question = input("Вы хотите увидеть список задач за текущий день? (да/нет): ")
    if question == 'нет':
        date = input("Введите дату в формате год-месяц-день: ")
    with conn:
        cursor = conn.execute(SQL_SELECT + " where planned=?", (date,))
        return cursor.fetchall()

def add_task(conn):
    name = input("Введите имя задачи: ")
    text = input("При желании, оставьте комментарий к задаче: ")
    date = dt.now().date()
    status = 'Не выполнено'
    with conn:
        conn.execute('''INSERT INTO diary(name, text, planned, status)
        VALUES (?, ?, ?, ?)''', (name, text, date, status))

def modify_task(conn):
    while True:
        id = int(input("Введите id задачи: "))
        result = find_id(conn, id)
        if result:
            with conn:
                new_name = input("Введите новое имя задачи: ")
                new_text = input("При желании, оставьте новый комментарий к задаче: ")
                conn.execute('''UPDATE diary SET name=?, text=?
                WHERE id=?''', (new_name, new_text, id))
                break
        else:
            print("Нет задачи с таким id")
            question = input("Хотите попробовать еще раз (да/нет): ")
            if question == 'нет':
                break

def change_status_done(conn):
    while True:
        id = int(input("Введите id задачи: "))
        result = find_id(conn, id)
        if result:
            with conn:
                status = 'Выполнено'
                conn.execute('''UPDATE diary SET status=? WHERE id=?''', (status, id))
                break
        else:
            print("Нет задачи с таким id")
            question = input("Хотите попробовать еще раз (да/нет): ")
            if question == 'нет':
                break

def change_status_undone(conn):
    while True:
        id = int(input("Введите id задачи: "))
        result = find_id(conn, id)
        if result:
            with conn:
                status = 'Не выполнено'
                conn.execute('''UPDATE diary SET status=? WHERE id=?''', (status, id))
                break
        else:
            print("Нет задачи с таким id")
            question = input("Хотите попробовать еще раз (да/нет): ")
            if question == 'нет':
                break
