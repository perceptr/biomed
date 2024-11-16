ALLOWED_EXTENSIONS = {'JPEG', 'JPG', 'PDF', 'PNG'}

def validate_document_extension(name: str):
    if name.split('.')[1].upper() not in ALLOWED_EXTENSIONS:
        raise Exception # не придумал, какое