import database as db
import logging
import logging_config

from help_func import *
from tests import testing, check_ans
from telebot import types
from qrcode import qr_code


logging_config.setup_logging()

db.create_users_table()
db.create_test_result_table()
db.create_course_step_table()


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message) -> None:
    """Обрабатывает команду /start и приветствует пользователя.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    logging.info(f"Received /start command from user {message.from_user.id}")

    if not db.get_user(message.from_user.id):
        bot.send_message(message.from_user.id, text=texts_tree['reg_fio'])
        logging.info(f"User {message.from_user.id} is not registered. Asking for FIO.")
        bot.register_next_step_handler(message, get_username)
    else:
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        bot.send_message(message.from_user.id, text=texts_tree['hello'].format(db.get_user(message.from_user.id)[2]),
                         reply_markup=inline_buttons)
        logging.info(f"User {message.from_user.id} is already registered. Sending menu.")
        bot.register_next_step_handler(message, send_menu)

    delete_last_messages(message)


def get_username(message: types.Message) -> None:
    """Получает ФИО пользователя и регистрирует его.

    Args:
        message (types.Message): Сообщение от пользователя с ФИО.
    """
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    db.insert_user(message.from_user.id, message.from_user.username, message.text)
    logging.info(f"Registered user {message.from_user.username} with ID {message.from_user.id}")

    bot.send_message(message.from_user.id, text=texts_tree['hello'].format(db.get_user(message.from_user.id)[2]),
                     reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.message_handler(commands=['help'])
def send_help(message: types.Message) -> None:
    """Обрабатывает команду /help и отправляет помощь пользователю.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    logging.info(f"Received /help command from user {message.from_user.id}")
    bot.send_message(message.from_user.id, texts_tree['help'])
    delete_last_messages(message.message)


@bot.message_handler(commands=['menu'])
def send_menu(message: types.Message) -> None:
    """Отправляет меню пользователю.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    logging.info(f"User {message.from_user.id} requested menu.")
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['menu'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.message_handler(content_types=['text'])
def wtf(message: types.Message) -> None:
    """Обрабатывает неожиданные текстовые сообщения от пользователя.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    logging.warning(f"Received unexpected text from user {message.from_user.id}: {message.text}")
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['wtf'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.callback_query_handler(lambda message: "menu" in message.data)
def redirect_menu(message: types.CallbackQuery) -> None:
    """Перенаправляет пользователя в меню.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя.
    """
    logging.info(f"User {message.from_user.id} redirected to menu.")
    delete_last_messages(message.message)
    send_menu(message)


@bot.callback_query_handler(lambda message: "theme" in message.data)
def view_theme(message: types.CallbackQuery) -> None:
    """Обрабатывает запрос на просмотр темы курса.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя.
    """
    theme_num = check_theme_num(message.data)
    db.update_course_step(theme_num, message.from_user.id, True)
    logging.info(f"User {message.from_user.id} viewed theme {theme_num}.")
    bot.send_message(message.from_user.id, text=COURSES[theme_num],
                     reply_markup=get_inline_button(edit_inline_button(theme_num, INLINE_VIEW_THEME, db, message)))
    delete_last_messages(message.message)


@bot.callback_query_handler(lambda message: "Test" in message.data)
def test(message: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало теста.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя.
    """
    logging.info(f"User {message.from_user.id} started a test.")
    delete_last_messages(message.message, False)
    testing(message)


@bot.callback_query_handler(lambda message: "pl" in message.data)
def check_answer(message: types.CallbackQuery) -> None:
    """Обрабатывает ответ пользователя на тест.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя.
    """
    logging.info(f"User {message.from_user.id} submitted an answer.")
    check_ans(message)
    delete_last_messages(message.message, False)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message: types.CallbackQuery) -> None:
    """Обрабатывает любые другие callback-запросы от пользователя.

    Args:
        message (types.CallbackQuery): Callback-запрос от пользователя.
    """
    logging.info(f"Processing callback from user {message.from_user.id}.")
    callbackk(message)


@bot.message_handler(content_types=["photo"])
def qrcode_worker(message: types.Message) -> None:
    """Обрабатывает фото, отправленное пользователем, и генерирует QR-код.

    Args:
        message (types.Message): Сообщение от пользователя с фото.
    """
    logging.info(f"User {message.from_user.id} sent a photo.")
    qr_code(message)


bot.infinity_polling()
