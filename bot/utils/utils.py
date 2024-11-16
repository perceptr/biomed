import os
from datetime import datetime
from random import randint

from aiogram.types import FSInputFile

from bot.create_bot import s3


def has_user_read_privacy_policy():
    return randint(1, 2) % 2

def is_user_registered():
    return randint(1, 2) % 2

def upload_image_to_s3(filename, key: str) -> None:
    s3.upload(filename, key)
    os.remove(filename)

def download_image_from_s3(key, filename):
    s3.download(key, filename)
    return FSInputFile(filename)


def add_data_to_key(key: str) -> str:
    date = datetime.now().strftime('%Y-%m-%d_%H:%M%S')
    return f'{key}_{date}'

def generate_tmp_filename(user_id: int) -> str:
    filename = f'/tmp/{add_data_to_key(str(user_id))}'
    os.open(filename, 644)
    return filename
