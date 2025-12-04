from typing import Literal, Optional, Callable, Union, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from .theme import get_theme
from .context import _ContextMixin, _auto_add_to_context, _parse_margin_padding


class Card(QFrame, _ContextMixin):
    clicked_signal = pyqtSignal()
    
    def __init__(self, variant: Literal['primary', 'secondary'] = 'secondary',
                 on_click: Optional[Callable] = None, parent=None,
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = 16):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self._variant = variant
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setObjectName("Card")
        
        margin_values = _parse_margin_padding(margin)
        padding_values = _parse_margin_padding(padding)
        self._margin = margin_values
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(*padding_values)
        self._layout.setSpacing(0)
        
        self.setMaximumHeight(300)
        self.setMaximumWidth(400)
        self._apply_style()
        
        if on_click:
            self.clicked_signal.connect(on_click)
        
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        theme = get_theme()
        
        if self._variant == 'primary':
            bg, hover = theme.primary, theme.primary_hover
            color = "#FFFFFF"
        else:
            bg, hover = theme.bg_secondary, theme.border
            color = theme.text
        
        margin_css = f"margin: {' '.join(map(str, self._margin))}px;"
        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {bg};
                border: 1px solid {theme.border};
                border-radius: 12px;
                {margin_css}
            }}
            QFrame#Card:hover {{
                background-color: {hover};
                border: 1px solid {theme.border};
            }}
            QFrame#Card > QLabel {{
                color: {color};
                background-color: transparent;
            }}
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked_signal.emit()
        super().mousePressEvent(event)
    
    def addWidget(self, widget: QWidget):
        """添加 widget 到卡片（用户自定义内容）"""
        self._layout.addWidget(widget)
