from typing import Union, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from .theme import Theme, set_theme
from .context import _ContextMixin, _auto_add_to_context, _parse_margin_padding


class Blocks(QWidget, _ContextMixin):
    def __init__(self, parent=None, theme: Union[str, Theme] = 'light',
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = 0):
        super().__init__(parent)
        self._theme = Theme(theme) if isinstance(theme, str) else (theme or Theme('light'))
        set_theme(self._theme)
        
        margin_values = _parse_margin_padding(margin)
        padding_values = _parse_margin_padding(padding)
        
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(*margin_values)
        self._main_layout.setSpacing(0)
        
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content = QWidget()
        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(*padding_values)
        self._layout.setSpacing(0)
        self._layout.addStretch()
        self._scroll.setWidget(content)
        
        self._main_layout.addWidget(self._scroll)
        self._apply_theme()
    
    def _apply_theme(self):
        scrollbar_color = "#CCCCCC" if self._theme.mode == 'light' else "#666666"
        scrollbar_hover = "#999999" if self._theme.mode == 'light' else "#888888"
        
        self.setStyleSheet(f"""
            QWidget {{ background-color: {self._theme.bg}; }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 11px;
            }}
            QScrollBar::handle:vertical {{
                background: {scrollbar_color};
                border-radius: 5px;
                min-height: 30px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {scrollbar_hover};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)
        
        for child in self.findChildren(QWidget):
            if hasattr(child, '_apply_style'):
                child._apply_style()
    
    def toggle_theme(self):
        self._theme = Theme('dark' if self._theme.mode == 'light' else 'light')
        set_theme(self._theme)
        self._apply_theme()
    
    def addWidget(self, widget: QWidget):
        self._layout.removeItem(self._layout.itemAt(self._layout.count() - 1))
        self._layout.addWidget(widget)
        self._layout.addStretch()
