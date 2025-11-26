from typing import Union
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from .theme import Theme
from .context import _ContextMixin, _auto_add_to_context


class Blocks(QWidget, _ContextMixin):
    def __init__(self, parent=None, theme: Union[str, Theme] = 'light'):
        # 初始化主窗口容器，设置滚动区域和主题
        super().__init__(parent)
        self._theme = Theme(theme) if isinstance(theme, str) else (theme or Theme('light'))
        
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content = QWidget()
        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(20)
        self._layout.addStretch()
        self._scroll.setWidget(content)
        
        self._main_layout.addWidget(self._scroll)
        self._apply_theme()
    
    def setHeader(self, header: QWidget):
        # 设置顶部导航栏
        self._main_layout.insertWidget(0, header)
    
    def _apply_theme(self):
        bg = self._theme.bg
        if self._theme.mode == 'light':
            scrollbar_color = "#CCCCCC"
            scrollbar_hover = "#999999"
        else:
            scrollbar_color = "#666666"
            scrollbar_hover = "#888888"
        
        self.setStyleSheet(f"""
            QWidget {{ background-color: {bg}; }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 11px;
                margin: 0px;
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
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)
        
        for child in self.findChildren(QWidget):
            if hasattr(child, '_apply_style'):
                child._apply_style()
    
    def toggle_theme(self):
        # 切换明暗主题
        self._theme = Theme('dark' if self._theme.mode == 'light' else 'light')
        self._apply_theme()
    
    def addWidget(self, widget: QWidget):
        # 添加 widget 到布局
        self._layout.removeItem(self._layout.itemAt(self._layout.count() - 1))
        self._layout.addWidget(widget)
        self._layout.addStretch()
