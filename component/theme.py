from typing import Literal
from PyQt6.QtWidgets import QWidget


class Theme:
    def __init__(self, mode: Literal['light', 'dark'] = 'light'):
        # 初始化主题，设置颜色值
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


def _get_theme(widget: QWidget) -> Theme:
    # 从 widget 树向上查找 Blocks 实例并返回其主题
    current = widget
    while current:
        if hasattr(current, '_theme') and hasattr(current, 'toggle_theme'):
            return current._theme
        current = current.parent()
    return Theme('light')
