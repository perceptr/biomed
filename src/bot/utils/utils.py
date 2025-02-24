import os
import re
from datetime import datetime
from time import time
from random import randint
from hashlib import sha256

from aiogram.types import FSInputFile

from src.bot.create_bot import s3
from src.schemas import GenderEnum, AnalysisSchema


def has_user_read_privacy_policy():
    return randint(1, 2) % 2


def is_user_registered():
    return randint(1, 2) % 2


async def upload_image_to_s3(filename, key: str) -> None:
    await s3.upload(filename, key)
    os.remove(filename)


async def download_image_from_s3(key, filename):
    await s3.download(key, filename)
    return FSInputFile(filename)


def add_data_to_key(key: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d_%H:%M%S")
    return f"{key}_{date}"


def generate_tmp_filename(user_id: int) -> str:
    filename = f"/tmp/{add_data_to_key(str(user_id))}"

    with open(filename, 'w') as file:
        pass

    os.chmod(filename, 0o644)

    return filename


def extract_number(text):
    match = re.search(r"\b(\d+)\b", text)
    if match:
        return int(match.group(1))
    else:
        return None


def get_gender_by_choice(choice: str):
    if choice == "uf_M":
        return GenderEnum.male
    elif choice == "uf_F":
        return GenderEnum.female
    else:
        raise KeyError

def generate_token():
    return sha256((str(time()).encode('utf-8'))).hexdigest()


async def get_analysis_photo(analysis: AnalysisSchema):
    tmp_file_name = generate_tmp_filename(analysis.user.telegram_id)
    photo = await download_image_from_s3(analysis.s3_address, tmp_file_name)
    return photo
