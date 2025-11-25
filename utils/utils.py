from datetime import datetime
import uuid


def generate_id():
    return str(uuid.uuid4())


def format_datetime(dt: datetime):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

