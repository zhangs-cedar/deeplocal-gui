from typing import Optional
from .button import Button
from .blocks import Blocks
from .theme import get_theme


class ThemeButton(Button):
    def __init__(self, blocks: Optional[Blocks] = None, parent=None):
        super().__init__("", 'secondary', parent)
        self._blocks = blocks or self._find_blocks()
        if not self._blocks:
            raise ValueError("需要 Blocks 实例")
        
        self._is_theme_button = True
        self.clicked_signal.connect(self._toggle_theme)
        self.setFixedSize(32, 32)
        self._apply_style()
        self._update_text()
    
    def _find_blocks(self) -> Optional[Blocks]:
        current = self.parent()
        while current:
            if isinstance(current, Blocks):
                return current
            current = current.parent()
        return None
    
    def _apply_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
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
    
    def _update_text(self):
        self.setText("🌙" if self._blocks._theme.mode == 'light' else "☀️")
    
    def _toggle_theme(self):
        self._blocks.toggle_theme()
        self._update_text()
        self._apply_style()
