import cv2
import random
import logging
import logging_config

from help_func import *
from pyzbar import pyzbar


logging_config.setup_logging()


def qr_code(message):
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
            logging.error(f"Не удалось загрузить изображение для пользователя {user_id}: {file_path}")
            bot.send_message(user_id, text="Ошибка при обработке изображения.")
            return

        # Декодирование QR-кодов
        barcodes = pyzbar.decode(img)

        if barcodes:
            for barcode in barcodes:
                barcodeData = barcode.data.decode('utf-8')
                logging.info(f'Результат декодирования для пользователя {user_id}: {barcodeData}')
                bot.send_message(user_id, text=barcodeData)
        else:
            logging.warning(f"QR-код не найден в изображении для пользователя {user_id}.")
            bot.send_message(user_id, text="QR-код не найден.")

    except Exception as e:
        logging.error(f"Произошла ошибка при обработке QR-кода для пользователя {user_id}: {e}")
        bot.send_message(user_id, text="Произошла ошибка при обработке вашего запроса.")