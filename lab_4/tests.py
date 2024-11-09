from help_func import *


token = open("token").readline()
bot = telebot.TeleBot(token)


def testing(message):
    logging.info(f"User {message.from_user.id} initiated a test with data: {message.data}")
    if message.data == "Test_places":
        gen_id_test(message, "test_files/public_test", "pl")
    elif message.data == "Test_qr":
        gen_id_test(message, "test_files/qr_test", "qr")
    elif message.data == "Test_phishing":
        gen_id_test(message, "test_files/phishing_test", "ph")
    elif message.data == "Test_social":
        gen_id_test(message, "test_files/social_test", "se")
    elif message.data == "Test_osint":
        gen_id_test(message, "test_files/test_osint", "osint")
    elif message.data == "Test_passwords":
        gen_id_test(message, "test_files/test_passwords", "ps")
    elif message.data == "Test_physical":
        gen_id_test(message, "test_files/phys_test", "pd")
    else:
        logging.warning(f"User {message.from_user.id} provided an unknown test type: {message.data}")


def check_ans(message):
    logging.info(f"User {message.from_user.id} submitted an answer with data: {message.data}")
    if "pl" in message.data:
        check_usr_ans(message, "test_files/public_test", score)
    elif "qr" in message.data:
        check_usr_ans(message, "qr_test", score)
    elif "ph" in message.data:
        check_usr_ans(message, "test_files/phishing_test", score)
    elif "se" in message.data:
        check_usr_ans(message, "test_files/social_test", score)
    elif "osing" in message.data:
        check_usr_ans(message, "test_files/test_osint", score)
    elif "ps" in message.data:
        check_usr_ans(message, "test_files/test_passwords", score)
    elif "pd" in message.data:
        check_usr_ans(message, "test_files/phys_test", score)
    else:
        logging.warning(f"User {message.from_user.id} submitted an answer for an unknown test type: {message.data}")
