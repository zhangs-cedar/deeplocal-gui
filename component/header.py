from typing import Union, Optional
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from .theme import _get_theme
from .blocks import Blocks
from .button import Button


class Header(QWidget):
    def __init__(self, title: str = "", icon: Union[str, Path] = None, avatar: Union[str, Path] = None, 
                 blocks: Optional[Blocks] = None, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._theme_btn = None
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)
        
        if icon:
            layout.addWidget(self._create_icon_label(icon))
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
            layout.addWidget(title_label)
        
        layout.addStretch()
        
        blocks_instance = blocks or self._find_blocks()
        if blocks_instance:
            self._theme_btn = self._create_theme_button(blocks_instance)
            layout.addWidget(self._theme_btn)
        
        if avatar:
            layout.addWidget(self._create_avatar_button(avatar))
        
        self._apply_style()
    
    def _find_blocks(self) -> Optional[Blocks]:
        current = self.parent()
        while current:
            if isinstance(current, Blocks):
                return current
            current = current.parent()
        return None
    
    def _create_icon_label(self, icon: Union[str, Path]) -> QLabel:
        icon_path = Path(icon) if isinstance(icon, str) else icon
        label = QLabel()
        if icon_path.exists():
            label.setPixmap(QIcon(str(icon_path)).pixmap(32, 32))
        else:
            label.setText(str(icon))
            label.setStyleSheet("font-size: 24px;")
        return label
    
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
    
    def _create_avatar_button(self, avatar: Union[str, Path]) -> QPushButton:
        avatar_path = Path(avatar) if isinstance(avatar, str) else avatar
        btn = QPushButton()
        if avatar_path.exists():
            pixmap = QPixmap(str(avatar_path))
            btn.setIcon(QIcon(pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        else:
            btn.setText(str(avatar))
        btn.setFixedSize(32, 32)
        btn.setStyleSheet("border-radius: 16px; border: none;")
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
            QPushButton {{ background-color: transparent; }}
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
