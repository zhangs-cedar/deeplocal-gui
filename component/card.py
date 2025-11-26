from typing import Literal, Union, Optional, Callable
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from .theme import _get_theme
from .context import _ContextMixin, _auto_add_to_context


class Card(QFrame, _ContextMixin):
    clicked_signal = pyqtSignal()
    
    def __init__(self, title: str = "", description: str = "", icon: Union[str, Path] = None, 
                 variant: Literal['primary', 'secondary'] = 'secondary', 
                 on_click: Optional[Callable] = None, parent=None):
        # 初始化卡片组件，设置图标、标题和描述
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self._variant = variant
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setObjectName("Card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        if icon:
            icon_label = QLabel()
            icon_path = Path(icon) if isinstance(icon, str) else icon
            if icon_path.exists():
                icon_label.setPixmap(QIcon(str(icon_path)).pixmap(32, 32))
            else:
                icon_label.setText(str(icon))
                icon_label.setStyleSheet("font-size: 24px;")
            layout.addWidget(icon_label)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 16px; font-weight: 600;")
            layout.addWidget(title_label)
        
        if description:
            desc = QLabel(description)
            desc.setWordWrap(True)
            desc.setStyleSheet("font-size: 13px; opacity: 0.7;")
            layout.addWidget(desc)
        
        layout.addStretch()
        self._apply_style()
        
        if on_click:
            self.clicked_signal.connect(on_click)
        
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        # 根据 variant 应用主题样式
        theme = _get_theme(self)
        bg, hover, color = (theme.primary, theme.primary_hover, "#FFFFFF") if self._variant == 'primary' else (theme.bg_secondary, theme.border, theme.text)
        self.setStyleSheet(f"""
            QFrame#Card {{ background-color: {bg}; border: 1px solid {theme.border}; border-radius: 12px; }}
            QFrame#Card:hover {{ background-color: {hover}; }}
            QFrame#Card > QLabel {{ color: {color}; background-color: transparent; }}
        """)
    
    def mousePressEvent(self, event):
        # 处理鼠标点击事件
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked_signal.emit()
        super().mousePressEvent(event)
    
    def click(self, fn=None):
        # 连接或返回点击信号
        return self.clicked_signal.connect(fn) if fn else self.clicked_signal
    
    def addWidget(self, widget: QWidget):
        # 添加 widget 到卡片布局
        self.layout().insertWidget(self.layout().count() - 1, widget)
