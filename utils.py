

from datetime import datetime
import uuid
from config import get_config


def generate_id():
    return str(uuid.uuid4())


def get_projects_dir():
    config = get_config()
    return config.get_projects_dir()


def format_datetime(dt: datetime):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

