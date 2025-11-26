from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from .theme import _get_theme
from .blocks import Blocks
from .button import Button
from .context import _ContextMixin


class Header(QWidget, _ContextMixin):
    def __init__(self, blocks: Optional[Blocks] = None, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._theme_btn = None
        
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
        
        blocks_instance = blocks or self._find_blocks()
        if blocks_instance:
            self._theme_btn = self._create_theme_button(blocks_instance)
            self.addRight(self._theme_btn)
        
        self._apply_style()
    
    def addLeft(self, widget: QWidget):
        self._left_layout.addWidget(widget)
    
    def addCenter(self, widget: QWidget):
        self._center_layout.addWidget(widget)
    
    def addRight(self, widget: QWidget):
        self._right_layout.addWidget(widget)
    
    def _find_blocks(self) -> Optional[Blocks]:
        current = self.parent()
        while current:
            if isinstance(current, Blocks):
                return current
            current = current.parent()
        return None
    
    def _create_theme_button(self, blocks: Blocks) -> Button:
        btn = Button("", 'secondary', self)
        btn._blocks = blocks
        btn._is_theme_button = True
        btn.clicked_signal.connect(lambda: self._toggle_theme(btn))
        btn.setFixedSize(32, 32)
        theme = _get_theme(self)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.bg_secondary};
                color: {theme.text};
                border: 1px solid {theme.border};
                border-radius: 4px;
                padding: 0px;
                font-size: 18px;
            }}
            QPushButton:hover {{ background-color: {theme.border}; }}
        """)
        self._update_theme_text(btn)
        return btn
    
    def _update_theme_text(self, btn: Button):
        btn.setText("🌙" if btn._blocks._theme.mode == 'light' else "☀️")
    
    def _toggle_theme(self, btn: Button):
        btn._blocks.toggle_theme()
        self._update_theme_text(btn)
    
    def _apply_style(self):
        theme = _get_theme(self)
        self.setStyleSheet(f"""
            QWidget {{ background-color: {theme.bg}; border-top: 1px solid #000000; border-bottom: 1px solid {theme.border}; }}
            QLabel {{ color: {theme.text}; }}
            QPushButton {{ background-color: transparent; color: {theme.text}; }}
        """)
        if self._theme_btn:
            self._theme_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.bg_secondary};
                    color: {theme.text};
                    border: 1px solid {theme.border};
                    border-radius: 4px;
                    padding: 0px;
                    font-size: 18px;
                }}
                QPushButton:hover {{ background-color: {theme.border}; }}
            """)
            self._update_theme_text(self._theme_btn)
