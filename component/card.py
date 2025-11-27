from typing import Literal, Union, Optional, Callable
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from .theme import get_theme
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
        
        from .theme import get_component_config
        
        card_config = get_component_config('card')
        padding = card_config.get('padding', 16)
        spacing = card_config.get('spacing', 8)
        max_width = card_config.get('max_width', 400)
        max_height = card_config.get('max_height', 300)
        title_font_size = card_config.get('title_font_size', 16)
        title_font_weight = card_config.get('title_font_weight', 600)
        desc_font_size = card_config.get('desc_font_size', 13)
        desc_opacity = card_config.get('desc_opacity', 0.7)
        icon_font_size = card_config.get('icon_font_size', 24)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(padding, padding, padding, padding)
        layout.setSpacing(spacing)
        
        if icon:
            icon_label = QLabel()
            icon_path = Path(icon) if isinstance(icon, str) else icon
            if icon_path.exists():
                icon_label.setPixmap(QIcon(str(icon_path)).pixmap(32, 32))
            else:
                icon_label.setText(str(icon))
                icon_label.setStyleSheet(f"font-size: {icon_font_size}px;")
            layout.addWidget(icon_label)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet(f"font-size: {title_font_size}px; font-weight: {title_font_weight};")
            layout.addWidget(title_label)
        
        if description:
            desc = QLabel(description)
            desc.setWordWrap(True)
            desc.setStyleSheet(f"font-size: {desc_font_size}px; opacity: {desc_opacity};")
            layout.addWidget(desc)
        
        layout.addStretch()
        self.setMaximumHeight(max_height)
        self.setMaximumWidth(max_width)
        self._apply_style()
        
        if on_click:
            self.clicked_signal.connect(on_click)
        
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        from .theme import get_theme, get_component_config
        
        theme = get_theme()
        card_config = get_component_config('card')
        
        # 从配置读取样式值，如果没有则使用默认值
        border_radius = card_config.get('border_radius', 12)
        padding = card_config.get('padding', 16)
        
        # 根据 variant 选择颜色
        if self._variant == 'primary':
            bg = theme.primary
            hover = theme.primary_hover
            variant_config = card_config.get('variants', {}).get('primary', {})
            color = variant_config.get('text_color', '#FFFFFF')
        else:
            bg = theme.bg_secondary
            hover = theme.border
            variant_config = card_config.get('variants', {}).get('secondary', {})
            color = variant_config.get('text_color') or theme.text
        
        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {bg};
                border: 1px solid {theme.border};
                border-radius: {border_radius}px;
                padding: {padding}px;
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
