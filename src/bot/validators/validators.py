from datetime import datetime

ALLOWED_EXTENSIONS = {"JPEG", "JPG", "PDF", "PNG"}


def validate_document_extension(name: str):
    if name.split(".")[1].upper() not in ALLOWED_EXTENSIONS:
        raise Exception  # не придумал, какое


def validate_year_of_birth(date: int | None):
    return date and (1900 <= date <= datetime.now().year)
