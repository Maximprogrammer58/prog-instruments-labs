import cv2
import random
import logging
import logging_config

from help_func import *
from telebot import types
from pyzbar import pyzbar


logging_config.setup_logging()


def qr_code(message: types.Message) -> None:
    """ Processes the image sent by the user and decodes the QR code.

    Args:
        message (types.Message): A message from the user containing an image with a QR code.
    """
    user_id = message.chat.id
    try:
        f_id = message.photo[-1].file_id
        file_name = bot.get_file(f_id)
        down_file = bot.download_file(file_name.file_path)

        number_qr = random.randint(1, 1000)
        file_path = f'img_{number_qr}.jpg'

        with open(file_path, 'wb') as file:
            file.write(down_file)

        img = cv2.imread(file_path)
        if img is None:
            logging.error(f"Failed to upload image for user {user_id}: {file_path}")
            bot.send_message(user_id, text="Ошибка при обработке изображения.")
            return

        barcodes = pyzbar.decode(img)

        if barcodes:
            for barcode in barcodes:
                barcodeData = barcode.data.decode('utf-8')
                logging.info(f'Decoding result for the user {user_id}: {barcodeData}')
                bot.send_message(user_id, text=barcodeData)
        else:
            logging.warning(f"The QR code was not found in the image for the user {user_id}.")
            bot.send_message(user_id, text="QR-код не найден.")

    except Exception as e:
        logging.error(f"An error occurred while processing the QR code for the user {user_id}: {e}")
        bot.send_message(user_id, text="Произошла ошибка при обработке вашего запроса.")
