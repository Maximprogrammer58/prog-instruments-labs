from help_func import *
from right_ans import check_usr_ans


token = open("token").readline()
bot = telebot.TeleBot(token)


def testing(message):
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


def check_ans(message):
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
