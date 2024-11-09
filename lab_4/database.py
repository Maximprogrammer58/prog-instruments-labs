import sqlite3


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_users_table():  # Создание таблицы пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, username TEXT, fullname TEXT)""")
    conn.commit()


def create_course_step_table():  # Создание таблицы, содержащей этап курса, на котором остановился пользователь
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS course_step (user_id INT, theme_0 BOOLEAN, theme_1 BOOLEAN, theme_2 BOOLEAN,
         theme_3 BOOLEAN, theme_4 BOOLEAN, theme_5 BOOLEAN, theme_6 BOOLEAN)""")
    conn.commit()


def insert_user(user_id: int, username: str, fullname: str):  # Добавление пользователя
    cursor.execute("""INSERT INTO users (user_id, username, fullname) VALUES (?, ?, ?)""",
                   (user_id, username, fullname))
    conn.commit()


def insert_course_step(theme_num, user_id: int,
                       theme_val: int):  # Добавление или замена этапа прохождения курса
    sql_text = """REPLACE INTO course_step (user_id, theme_{}) VALUES (?, ?)""".format(theme_num)
    cursor.execute(sql_text, (user_id, theme_val))
    conn.commit()


def update_course_step(theme_num, user_id: int,
                       theme_val: int):  # Добавление или замена этапа прохождения курса
    sql_text = """UPDATE course_step SET theme_{} = ? WHERE user_id = ?""".format(theme_num)
    cursor.execute(sql_text, (theme_val, user_id))
    conn.commit()


def get_all_users():  # Получение всех пользователей
    cursor.execute("""SELECT * FROM users """)
    return cursor.fetchall()


def get_user(user_id: int):  # Получение информации о пользователе
    cursor.execute("""SELECT * FROM users WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def get_result(user_id: int):  # Получение информации о результате прохождения теста
    cursor.execute("""SELECT * FROM test_result WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def get_all_results():  # Получение всех результатов прохождения теста
    cursor.execute("""SELECT * FROM test_result """)
    return cursor.fetchall()


def get_course_step(user_id: int):  # Получение информации о этапе курса
    cursor.execute("""SELECT * FROM course_step WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def create_test_result_table():  # Создание таблицы результатов тестирований
    cursor.execute("""CREATE TABLE IF NOT EXISTS test_result (user_id INT,  theme_0 INT, theme_1 INT, theme_2 INT,
         theme_3 INT, theme_4 INT, theme_5 INT, theme_6 INT)""")
    conn.commit()


def insert_test_result(user_id: int):  # Добавление результата тестирования
    cursor.execute("""INSERT INTO test_result (user_id, theme_0, theme_1, theme_2,
         theme_3, theme_4, theme_5, theme_6 ) VALUES ( (?), 0, 0, 0, 0, 0, 0, 0)""", (user_id,))
    conn.commit()


def get_result(user_id: int):  # Получение информации о результате прохождения теста
    cursor.execute("""SELECT * FROM test_result WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def update_test_result(theme, user_id: int, theme_val: int):  # Добавление или замена этапа прохождения курса
    sql_text = """UPDATE test_result SET {} = ? WHERE user_id = ?""".format(theme)
    cursor.execute(sql_text, (theme_val, user_id))
    conn.commit()
