import cv2
import random

from help_func import *
from pyzbar import pyzbar


def qr_code(message):
    f_id = message.photo[len(message.photo) - 1].file_id
    file_name = bot.get_file(f_id)
    down_file = bot.download_file(file_name.file_path)
    number_qr = random.randint(1, 1000)
    with open(f'img_{number_qr}' + '.jpg', 'wb') as file:
        file.write(down_file)
    img = cv2.imread(f"img_{number_qr}.jpg")
    barcodes = pyzbar.decode(img)

    for barcode in barcodes:
        barcodeData = barcode.data.decode('utf-8')
        print(f'Result: {barcodeData}')
        bot.send_message(message.chat.id, text=barcodeData)