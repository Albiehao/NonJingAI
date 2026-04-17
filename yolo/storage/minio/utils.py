import uuid

def generate_filename(filename: str):
    ext = filename.split(".")[-1]
    return f"{uuid.uuid4()}.{ext}"