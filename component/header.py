from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from .theme import get_theme
from .context import _ContextMixin


class Header(QWidget, _ContextMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 0)
        main_layout.setSpacing(16)
        
        self._left_layout = QHBoxLayout()
        self._left_layout.setSpacing(16)
        self._left_layout.setContentsMargins(0, 0, 0, 0)
        
        self._center_layout = QHBoxLayout()
        self._center_layout.setSpacing(16)
        self._center_layout.setContentsMargins(0, 0, 0, 0)
        
        self._right_layout = QHBoxLayout()
        self._right_layout.setSpacing(16)
        self._right_layout.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addLayout(self._left_layout)
        main_layout.addStretch()
        main_layout.addLayout(self._center_layout)
        main_layout.addStretch()
        main_layout.addLayout(self._right_layout)
        
        self._apply_style()
    
    def addLeft(self, widget: QWidget):
        self._left_layout.addWidget(widget)
    
    def addCenter(self, widget: QWidget):
        self._center_layout.addWidget(widget)
    
    def addRight(self, widget: QWidget):
        self._right_layout.addWidget(widget)
    
    def _apply_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            QWidget {{ background-color: {theme.bg}; border-top: 1px solid #000000; border-bottom: 1px solid {theme.border}; }}
            QLabel {{ color: {theme.text}; }}
            QPushButton {{ background-color: transparent; color: {theme.text}; }}
        """)
