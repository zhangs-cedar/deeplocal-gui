from typing import Literal, Optional, Callable, Union, Tuple
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from .theme import get_theme
from .context import _auto_add_to_context, _parse_margin_padding


class Button(QPushButton):
    clicked_signal = pyqtSignal()
    
    def __init__(self, value: str = "Run", variant: Literal['primary', 'secondary', 'text'] = 'secondary', 
                 on_click: Optional[Callable] = None, parent=None,
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = (8, 20)):
        super().__init__(str(value), parent)
        self._variant = variant
        self._margin = _parse_margin_padding(margin)
        self._padding = _parse_margin_padding(padding)
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
        theme = get_theme()
        if self._variant == 'primary':
            bg, hover, color = theme.primary, theme.primary_hover, "#FFFFFF"
            border = f"1px solid {theme.border}"
        elif self._variant == 'text':
            bg, hover, color = "transparent", theme.bg_secondary, theme.text
            border = "none"
        else:
            bg, hover, color = theme.bg_secondary, theme.border, theme.text
            border = f"1px solid {theme.border}"
        
        margin_css = f"margin: {' '.join(map(str, self._margin))}px;"
        padding_css = f"padding: {self._padding[0]}px {self._padding[1]}px;"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: {border};
                border-radius: 8px;
                {padding_css}
                {margin_css}
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
