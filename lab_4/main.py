import database as db

from help_func import *
from tests import testing, check_ans
from qrcode import qr_code


db.create_users_table()
db.create_test_result_table()
db.create_course_step_table()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # проверка на зарег, если зарег выдать меню
    def get_username(message):  # получаем ФИО
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        db.insert_user(message.from_user.id, message.from_user.username, message.text)
        bot.send_message(message.from_user.id, text=texts_tree['hello'].format(db.get_user(message.from_user.id)[2]),
                         reply_markup=inline_buttons)
        delete_last_messages(message)

    if not db.get_user(message.from_user.id):
        bot.send_message(message.from_user.id, text=texts_tree['reg_fio'])
        bot.register_next_step_handler(message, get_username)
    else:
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        bot.send_message(message.from_user.id, text=texts_tree['hello'].format(db.get_user(message.from_user.id)[2]),
                         reply_markup=inline_buttons)
        bot.register_next_step_handler(message, send_menu)
    delete_last_messages(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, texts_tree['help'])
    delete_last_messages(message.message)


@bot.message_handler(commands=['menu'])  # реагирует на любую надпись в чате
def send_menu(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['menu'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.message_handler(content_types=['text'])  # реагирует на любую надпись в чате
def wtf(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['wtf'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.callback_query_handler(lambda message: "menu" in message.data)
def redirect_menu(message):
    delete_last_messages(message.message)
    send_menu(message)


@bot.callback_query_handler(lambda message: "theme" in message.data)
def view_theme(message):
    theme_num = check_theme_num(message.data)
    db.update_course_step(theme_num, message.from_user.id, True)
    bot.send_message(message.from_user.id, text=COURSES[theme_num],
                     reply_markup=get_inline_button(edit_inline_button(theme_num, INLINE_VIEW_THEME, db, message)))
    delete_last_messages(message.message)


@bot.callback_query_handler(lambda message: "Test" in message.data)
def test(message):
    delete_last_messages(message.message, False)
    testing(message)


@bot.callback_query_handler(lambda message: "pl" in message.data)
def check_answer(message):
    check_ans(message)
    delete_last_messages(message.message, False)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message):
    callbackk(message)


@bot.message_handler(content_types=["photo"])
def qrcode_worker(message):
    qr_code(message)


bot.infinity_polling()