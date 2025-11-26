from typing import Literal
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from .theme import _get_theme
from .context import _auto_add_to_context


class Button(QPushButton):
    clicked_signal = pyqtSignal()
    
    def __init__(self, value: str = "Run", variant: Literal['primary', 'secondary'] = 'secondary', parent=None):
        # 初始化按钮，设置样式和信号连接
        super().__init__(str(value), parent)
        self._variant = variant
        self.clicked.connect(self._on_clicked)
        self._apply_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        # 根据 variant 应用主题样式
        theme = _get_theme(self)
        if self._variant == 'primary':
            bg, hover, color = theme.primary, theme.primary_hover, "#FFFFFF"
        else:
            bg, hover, color = theme.bg_secondary, theme.border, theme.text
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: 1px solid {theme.border};
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
        """)
    
    def _on_clicked(self):
        # 点击时发射自定义信号
        self.clicked_signal.emit()
    
    def click(self, fn=None):
        # 连接或返回点击信号
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal
