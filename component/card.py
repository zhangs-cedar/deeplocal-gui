from typing import Literal, Optional, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from .theme import get_theme, get_component_config
from .context import _ContextMixin, _auto_add_to_context


class Card(QFrame, _ContextMixin):
    clicked_signal = pyqtSignal()
    
    def __init__(self, variant: Literal['primary', 'secondary'] = 'secondary',
                 on_click: Optional[Callable] = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self._variant = variant
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setObjectName("Card")
        
        cfg = get_component_config('card')
        padding = cfg.get('padding', 16)
        spacing = cfg.get('spacing', 8)
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(padding, padding, padding, padding)
        self._layout.setSpacing(spacing)
        
        self.setMaximumHeight(cfg.get('max_height', 300))
        self.setMaximumWidth(cfg.get('max_width', 400))
        self._apply_style()
        
        if on_click:
            self.clicked_signal.connect(on_click)
        
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        theme = get_theme()
        cfg = get_component_config('card')
        variant_cfg = cfg.get('variants', {}).get(self._variant, {})
        
        if self._variant == 'primary':
            bg, hover = theme.primary, theme.primary_hover
            color = variant_cfg.get('text_color', '#FFFFFF')
        else:
            bg, hover = theme.bg_secondary, theme.border
            color = variant_cfg.get('text_color') or theme.text
        
        border_radius = cfg.get('border_radius', 12)
        
        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {bg};
                border: 1px solid {theme.border};
                border-radius: {border_radius}px;
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
