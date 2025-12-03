from typing import Literal
import os
import yaml
from pathlib import Path

FILE = os.path.join(os.path.dirname(__file__), 'theme.yaml')


class Theme:
    def __init__(self, mode: Literal['light', 'dark'] = 'light'):
        self.mode = mode
        if mode == 'light':
            self.bg = "#FFFFFF"
            self.bg_secondary = "#F5F5F7"
            self.text = "#000000"
            self.text_secondary = "#6E6E73"
            self.primary = "#007AFF"
            self.primary_hover = "#0051D5"
            self.border = "#D1D1D6"
        else:
            self.bg = "#1C1C1E"
            self.bg_secondary = "#2C2C2E"
            self.text = "#FFFFFF"
            self.text_secondary = "#98989D"
            self.primary = "#0A84FF"
            self.primary_hover = "#409CFF"
            self.border = "#38383A"


def _load_config() -> dict:
    path = os.environ.get('THEME_FILE', FILE)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, IOError):
            pass
    return {'theme': 'light'}


def _save_config(config: dict):
    path = os.environ.get('THEME_FILE', FILE)
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    except IOError:
        pass


def get_theme() -> Theme:
    return Theme(_load_config().get('theme', 'light'))


def set_theme(theme: Theme):
    """设置主题，保留其他配置"""
    config = _load_config()
    config['theme'] = theme.mode
    _save_config(config)
