import sqlite3
import logging
import logging_config


logging_config.setup_logging()

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_users_table() -> None:
    """Creates a user table if it does not exist."""
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, username TEXT, fullname TEXT)""")
        conn.commit()
        logging.info("The user table has been successfully created or already exists.")
    except Exception as e:
        logging.error(f"Error creating the user table: {e}")


def create_course_step_table() -> None:
    """Creates a table of course stages if it does not exist."""
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS course_step (user_id INT, theme_0 BOOLEAN, theme_1 BOOLEAN, theme_2 BOOLEAN,
             theme_3 BOOLEAN, theme_4 BOOLEAN, theme_5 BOOLEAN, theme_6 BOOLEAN)""")
        conn.commit()
        logging.info("The course stage table has been successfully created or already exists.")
    except Exception as e:
        logging.error(f"Error creating the course stage table: {e}")


def insert_user(user_id: int, username: str, fullname: str) -> None:
    """Adds a user to the users table.

    Args:
        user_id (int): User ID.
        username (user): The user's name.
        fullname (string): The full name of the user.
    """
    try:
        cursor.execute("""INSERT INTO users (user_id, username, fullname) VALUES (?, ?, ?)""",
                       (user_id, username, fullname))
        conn.commit()
        logging.info(f"The user {username} (ID: {user_id}) has been successfully added.")
    except Exception as e:
        logging.error(f"Error when adding a user {username}: {e}")


def insert_course_step(theme_num: int, user_id: int, theme_val: int) -> None:
    """ Adds or replaces a course completion stage for the user.

        Args:
            theme_num (int): The topic number.
            user_id (int): User ID.
            theme_val (int): The meaning of the topic.
    """
    try:
        sql_text = """REPLACE INTO course_step (user_id, theme_{}) VALUES (?, ?)""".format(theme_num)
        cursor.execute(sql_text, (user_id, theme_val))
        conn.commit()
        logging.info(f"The {theme_num} course stage for the {user_id} user has been successfully updated.")
    except Exception as e:
        logging.error(f"Error updating the course stage for the user {user_id}: {e}")


def update_course_step(theme_num: int, user_id: int, theme_val: int) -> None:
    """Updates the course completion stage for the user.

    Args:
        theme_num (int): The topic number.
        user_id (int): User ID.
        theme_val (int): The new meaning of the theme.
    """
    try:
        sql_text = """UPDATE course_step SET theme_{} = ? WHERE user_id = ?""".format(theme_num)
        cursor.execute(sql_text, (theme_val, user_id))
        conn.commit()
        logging.info(f"The {theme_num} course stage for the {user_id} user has been successfully updated.")
    except Exception as e:
        logging.error(f"Error updating the course stage for the user {user_id}: {e}")


def get_all_users() -> list:
    """Gets all users from the users table.

    Returns:
        list: A list of all users.
    """
    try:
        cursor.execute("""SELECT * FROM users """)
        users = cursor.fetchall()
        logging.info("All users from the database have been retrieved.")
        return users
    except Exception as e:
        logging.error(f"Error receiving all users: {e}")
        return []


def get_user(user_id: int) -> tuple | None:
    """ Gets information about the user by his ID.

        Args:
            user_id (int): User ID.

        Returns:
            tuple | None: User information or None if the user is not found.
    """
    try:
        cursor.execute("""SELECT * FROM users WHERE user_id = (?)""", (user_id,))
        user = cursor.fetchone()
        logging.info(f"Information about the user ID was received: {user_id}.")
        return user
    except Exception as e:
        logging.error(f"Error receiving user information {user_id}: {e}")
        return None


def get_result(user_id: int) -> tuple | None:
    """Gets the test result for the user.

    Args:
        user_id (int): User ID.

    Returns:
        tuple | None: Test result or None if no result is found.
    """
    try:
        cursor.execute("""SELECT * FROM test_result WHERE user_id = (?)""", (user_id,))
        result = cursor.fetchone()
        logging.info(f"The test result was received for the user ID: {user_id}.")
        return result
    except Exception as e:
        logging.error(f"Error when receiving the test result for the user {user_id}: {e}")
        return None


def get_all_results() -> list:
    """Retrieves all test results from the database.

    Returns:
        list: A list of all test results.
    """
    try:
        cursor.execute("""SELECT * FROM test_result """)
        results = cursor.fetchall()
        logging.info("All test results have been obtained from the database.")
        return results
    except Exception as e:
        logging.error(f"Error when receiving all test results: {e}")
        return []


def get_course_step(user_id: int) -> tuple | None:
    """ Gets information about the current stage of the course for the user.

    Args:
        user_id (int): User ID.

    Returns:
        type | None: Information about the course stage, or None if the stage is not found.
    """
    try:
        cursor.execute("""SELECT * FROM course_step WHERE user_id = (?)""", (user_id,))
        course_step = cursor.fetchone()
        logging.info(f"Information about the course stage was received for the user ID: {user_id}.")
        return course_step
    except Exception as e:
        logging.error(f"Error when receiving the course stage for the user {user_id}: {e}")
        return None


def create_test_result_table() -> None:  # Создание таблицы результатов тестирований
    """Creates a table of test results if it does not exist."""
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS test_result (user_id INT,  theme_0 INT, theme_1 INT, theme_2 INT,
             theme_3 INT, theme_4 INT, theme_5 INT, theme_6 INT)""")
        conn.commit()
        logging.info("The test results table has been successfully created or already exists.")
    except Exception as e:
        logging.error(f"Error when creating the test results table: {e}")


def insert_test_result(user_id: int) -> None:
    """Adds the test result for the user.

    Args:
        user_id (int): User ID.
    """
    try:
        cursor.execute("""INSERT INTO test_result (user_id, theme_0, theme_1, theme_2,
             theme_3, theme_4, theme_5, theme_6 ) VALUES (?, 0, 0, 0, 0, 0, 0, 0)""", (user_id,))
        conn.commit()
        logging.info(f"The test results for user ID: {user_id} have been successfully added.")
    except Exception as e:
        logging.error(f"Error when adding test results for user {user_id}: {e}")


def update_test_result(theme: str, user_id: int, theme_val: int) -> None:
    """Updates the test result for the user.

    Args:
        theme (str): The name of the theme.
        user_id (int): The user ID.
        theme_val (int): The new meaning of the theme.
    """
    try:
        sql_text = """UPDATE test_result SET {} = ? WHERE user_id = ?""".format(theme)
        cursor.execute(sql_text, (theme_val, user_id))
        conn.commit()
        logging.info(f"The test result for user ID: {user_id} has been successfully updated.")
    except Exception as e:
        logging.error(f"Error updating the test result for the user {user_id}: {e}")
