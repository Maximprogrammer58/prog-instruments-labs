import telebot
import logging
import logging_config

from help_func import *
from telebot import types


token = open("token").readline().strip()
bot = telebot.TeleBot(token)

logging_config.setup_logging()


def testing(message: types.CallbackQuery) -> None:
    """Обрабатывает запрос пользователя на начало теста.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя с информацией о тесте.
    """
    logging.info(f"User {message.from_user.id} initiated a test with data: {message.data}")

    test_mapping = {
        "Test_places": ("test_files/public_test", "pl"),
        "Test_qr": ("test_files/qr_test", "qr"),
        "Test_phishing": ("test_files/phishing_test", "ph"),
        "Test_social": ("test_files/social_test", "se"),
        "Test_osint": ("test_files/test_osint", "osint"),
        "Test_passwords": ("test_files/test_passwords", "ps"),
        "Test_physical": ("test_files/phys_test", "pd"),
    }

    if message.data in test_mapping:
        gen_id_test(message, *test_mapping[message.data])
    else:
        logging.warning(f"User {message.from_user.id} provided an unknown test type: {message.data}")


def check_ans(message: types.CallbackQuery) -> None:
    """Проверяет ответ пользователя на тест.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя с данными ответа.
    """
    logging.info(f"User {message.from_user.id} submitted an answer with data: {message.data}")

    answer_mapping = {
        "pl": "test_files/public_test",
        "qr": "qr_test",
        "ph": "test_files/phishing_test",
        "se": "test_files/social_test",
        "osing": "test_files/test_osint",
        "ps": "test_files/test_passwords",
        "pd": "test_files/phys_test",
    }

    for key in answer_mapping.keys():
        if key in message.data:
            check_usr_ans(message, answer_mapping[key], score)
            return

    logging.warning(f"User {message.from_user.id} submitted an answer for an unknown test type: {message.data}")
