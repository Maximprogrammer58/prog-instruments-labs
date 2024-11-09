import sqlite3
import logging
import logging_config


logging_config.setup_logging()

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_users_table() -> None:  # Создание таблицы пользователей
    """Создает таблицу пользователей, если она не существует."""
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, username TEXT, fullname TEXT)""")
        conn.commit()
        logging.info("Таблица пользователей успешно создана или уже существует.")
    except Exception as e:
        logging.error(f"Ошибка при создании таблицы пользователей: {e}")


def create_course_step_table() -> None:  # Создание таблицы, содержащей этап курса
    """Создает таблицу этапов курса, если она не существует."""
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS course_step (user_id INT, theme_0 BOOLEAN, theme_1 BOOLEAN, theme_2 BOOLEAN,
             theme_3 BOOLEAN, theme_4 BOOLEAN, theme_5 BOOLEAN, theme_6 BOOLEAN)""")
        conn.commit()
        logging.info("Таблица этапов курса успешно создана или уже существует.")
    except Exception as e:
        logging.error(f"Ошибка при создании таблицы этапов курса: {e}")


def insert_user(user_id: int, username: str, fullname: str) -> None:  # Добавление пользователя
    """Добавляет пользователя в таблицу users.

    Args:
        user_id (int): Идентификатор пользователя.
        username (str): Имя пользователя.
        fullname (str): Полное имя пользователя.
    """
    try:
        cursor.execute("""INSERT INTO users (user_id, username, fullname) VALUES (?, ?, ?)""",
                       (user_id, username, fullname))
        conn.commit()
        logging.info(f"Пользователь {username} (ID: {user_id}) успешно добавлен.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении пользователя {username}: {e}")


def insert_course_step(theme_num: int, user_id: int, theme_val: int) -> None:  # Добавление или замена этапа прохождения курса
    """Добавляет или заменяет этап прохождения курса для пользователя.

    Args:
        theme_num (int): Номер темы.
        user_id (int): Идентификатор пользователя.
        theme_val (int): Значение темы.
    """
    try:
        sql_text = """REPLACE INTO course_step (user_id, theme_{}) VALUES (?, ?)""".format(theme_num)
        cursor.execute(sql_text, (user_id, theme_val))
        conn.commit()
        logging.info(f"Этап курса {theme_num} для пользователя {user_id} успешно обновлён.")
    except Exception as e:
        logging.error(f"Ошибка при обновлении этапа курса для пользователя {user_id}: {e}")


def update_course_step(theme_num: int, user_id: int, theme_val: int) -> None:  # Обновление этапа прохождения курса
    """Обновляет этап прохождения курса для пользователя.

    Args:
        theme_num (int): Номер темы.
        user_id (int): Идентификатор пользователя.
        theme_val (int): Новое значение темы.
    """
    try:
        sql_text = """UPDATE course_step SET theme_{} = ? WHERE user_id = ?""".format(theme_num)
        cursor.execute(sql_text, (theme_val, user_id))
        conn.commit()
        logging.info(f"Этап курса {theme_num} для пользователя {user_id} успешно обновлён.")
    except Exception as e:
        logging.error(f"Ошибка при обновлении этапа курса для пользователя {user_id}: {e}")


def get_all_users() -> list:  # Получение всех пользователей
    """Получает всех пользователей из таблицы users.

    Returns:
        list: Список всех пользователей.
    """
    try:
        cursor.execute("""SELECT * FROM users """)
        users = cursor.fetchall()
        logging.info("Получены все пользователи из базы данных.")
        return users
    except Exception as e:
        logging.error(f"Ошибка при получении всех пользователей: {e}")
        return []


def get_user(user_id: int) -> tuple | None:  # Получение информации о пользователе
    """Получает информацию о пользователе по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        tuple | None: Информация о пользователе или None, если пользователь не найден.
    """
    try:
        cursor.execute("""SELECT * FROM users WHERE user_id = (?)""", (user_id,))
        user = cursor.fetchone()
        logging.info(f"Получена информация о пользователе ID: {user_id}.")
        return user
    except Exception as e:
        logging.error(f"Ошибка при получении информации о пользователе {user_id}: {e}")
        return None


def get_result(user_id: int) -> tuple | None:  # Получение информации о результате прохождения теста
    """Получает результат теста для пользователя.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        tuple | None: Результат теста или None, если результат не найден.
    """
    try:
        cursor.execute("""SELECT * FROM test_result WHERE user_id = (?)""", (user_id,))
        result = cursor.fetchone()
        logging.info(f"Получен результат теста для пользователя ID: {user_id}.")
        return result
    except Exception as e:
        logging.error(f"Ошибка при получении результата теста для пользователя {user_id}: {e}")
        return None


def get_all_results() -> list:  # Получение всех результатов прохождения теста
    """Получает все результаты тестов из базы данных.

    Returns:
        list: Список всех результатов тестов.
    """
    try:
        cursor.execute("""SELECT * FROM test_result """)
        results = cursor.fetchall()
        logging.info("Получены все результаты тестов из базы данных.")
        return results
    except Exception as e:
        logging.error(f"Ошибка при получении всех результатов тестов: {e}")
        return []


def get_course_step(user_id: int) -> tuple | None:  # Получение информации о этапе курса
    """Получает информацию о текущем этапе курса для пользователя.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        tuple | None: Информация о этапе курса или None, если этап не найден.
    """
    try:
        cursor.execute("""SELECT * FROM course_step WHERE user_id = (?)""", (user_id,))
        course_step = cursor.fetchone()
        logging.info(f"Получена информация о этапе курса для пользователя ID: {user_id}.")
        return course_step
    except Exception as e:
        logging.error(f"Ошибка при получении этапа курса для пользователя {user_id}: {e}")
        return None


def create_test_result_table() -> None:  # Создание таблицы результатов тестирований
    """Создает таблицу результатов тестирования, если она не существует."""
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS test_result (user_id INT,  theme_0 INT, theme_1 INT, theme_2 INT,
             theme_3 INT, theme_4 INT, theme_5 INT, theme_6 INT)""")
        conn.commit()
        logging.info("Таблица результатов тестирований успешно создана или уже существует.")
    except Exception as e:
        logging.error(f"Ошибка при создании таблицы результатов тестирований: {e}")


def insert_test_result(user_id: int) -> None:  # Добавление результата тестирования
    """Добавляет результат тестирования для пользователя.

    Args:
        user_id (int): Идентификатор пользователя.
    """
    try:
        cursor.execute("""INSERT INTO test_result (user_id, theme_0, theme_1, theme_2,
             theme_3, theme_4, theme_5, theme_6 ) VALUES (?, 0, 0, 0, 0, 0, 0, 0)""", (user_id,))
        conn.commit()
        logging.info(f"Результаты тестирования для пользователя ID: {user_id} успешно добавлены.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении результатов тестирования для пользователя {user_id}: {e}")


def update_test_result(theme: str, user_id: int, theme_val: int) -> None:  # Обновление результата тестирования
    """Обновляет результат тестирования для пользователя.

    Args:
        theme (str): Название темы.
        user_id (int): Идентификатор пользователя.
        theme_val (int): Новое значение темы.
    """
    try:
        sql_text = """UPDATE test_result SET {} = ? WHERE user_id = ?""".format(theme)
        cursor.execute(sql_text, (theme_val, user_id))
        conn.commit()
        logging.info(f"Результат тестирования для пользователя ID: {user_id} успешно обновлён.")
    except Exception as e:
        logging.error(f"Ошибка при обновлении результата тестирования для пользователя {user_id}: {e}")
