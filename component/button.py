from typing import Literal, Optional, Callable
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from .theme import _get_theme
from .context import _auto_add_to_context


class Button(QPushButton):
    clicked_signal = pyqtSignal()
    
    def __init__(self, value: str = "Run", variant: Literal['primary', 'secondary', 'text'] = 'secondary', 
                 on_click: Optional[Callable] = None, parent=None):
        super().__init__(str(value), parent)
        self._variant = variant
        self.clicked.connect(self._on_clicked)
        self._apply_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_click:
            self.clicked_signal.connect(on_click)
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        # 跳过主题按钮，由 Header 管理其样式
        if hasattr(self, '_is_theme_button') and self._is_theme_button:
            return
        # 根据 variant 应用主题样式
        theme = _get_theme(self)
        if self._variant == 'primary':
            bg, hover, color = theme.primary, theme.primary_hover, "#FFFFFF"
            border = f"1px solid {theme.border}"
        elif self._variant == 'text':
            bg, hover, color = "transparent", theme.bg_secondary, theme.text
            border = "none"
        else:
            bg, hover, color = theme.bg_secondary, theme.border, theme.text
            border = f"1px solid {theme.border}"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: {border};
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
        """)
    
    def _on_clicked(self):
        self.clicked_signal.emit()
    
    def click(self, fn=None):
        # 连接或返回点击信号
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal
