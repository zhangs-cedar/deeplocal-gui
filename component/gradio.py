from typing import Optional, Literal, Callable, List, Union
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, QEvent, pyqtSignal, QUrl
from PyQt6.QtGui import QEnterEvent, QIcon, QDesktopServices

_context_stack: List[QWidget] = []


class Theme:
    def __init__(self, mode: Literal['light', 'dark'] = 'light'):
        """初始化主题"""
        self.mode = mode
        if mode == 'light':
            self.background = "#FFFFFF"
            self.background_secondary = "#F8F9FA"
            self.background_tertiary = "#E8E9EA"
            self.border = "#E0E0E0"
            self.border_hover = "#D0D1D2"
            self.text = "#1F2937"
            self.text_secondary = "#6B7280"
            self.primary = "#6366F1"
            self.primary_hover = "#4F46E5"
            self.primary_pressed = "#4338CA"
            self.secondary = "#FFFFFF"
            self.secondary_border = "#D1D5DB"
            self.secondary_hover = "#F9FAFB"
            self.secondary_pressed = "#F3F4F6"
            self.stop = "#EF4444"
            self.stop_hover = "#DC2626"
            self.stop_pressed = "#B91C1C"
            self.panel_bg = "#F8F9FA"
            self.panel_bg_hover = "#E8E9EA"
            self.panel_border = "#E0E0E0"
            self.panel_border_hover = "#D0D1D2"
            self.tab_bg = "#F8F9FA"
            self.tab_selected_bg = "#FFFFFF"
            self.tab_text = "#6B7280"
            self.tab_text_selected = "#1F2937"
            self.tab_border = "#6366F1"
        else:
            self.background = "#1E1E1E"
            self.background_secondary = "#2D2D2D"
            self.background_tertiary = "#3D3D3D"
            self.border = "#404040"
            self.border_hover = "#505050"
            self.text = "#E5E5E5"
            self.text_secondary = "#A0A0A0"
            self.primary = "#6366F1"
            self.primary_hover = "#818CF8"
            self.primary_pressed = "#4F46E5"
            self.secondary = "#2D2D2D"
            self.secondary_border = "#404040"
            self.secondary_hover = "#3D3D3D"
            self.secondary_pressed = "#353535"
            self.stop = "#EF4444"
            self.stop_hover = "#F87171"
            self.stop_pressed = "#DC2626"
            self.panel_bg = "#2D2D2D"
            self.panel_bg_hover = "#3D3D3D"
            self.panel_border = "#404040"
            self.panel_border_hover = "#505050"
            self.tab_bg = "#2D2D2D"
            self.tab_selected_bg = "#1E1E1E"
            self.tab_text = "#A0A0A0"
            self.tab_text_selected = "#E5E5E5"
            self.tab_border = "#6366F1"


def _get_theme(widget: QWidget) -> Theme:
    """从组件树向上查找主题"""
    current = widget
    while current:
        if isinstance(current, Blocks):
            return current._theme
        current = current.parent()
    return Theme('light')


def _auto_add_to_context(widget: QWidget):
    """自动将组件添加到当前上下文"""
    if widget.parent() or not _context_stack:
        return
    current = _context_stack[-1]
    if isinstance(current, Row):
        stretch = widget.get_scale() if isinstance(widget, Column) else 0
        current.addWidget(widget, stretch)
    elif isinstance(current, (Column, Group, Blocks)):
        current.addWidget(widget)


class _ContextMixin:
    def __enter__(self):
        """进入上下文"""
        _context_stack.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False


class _VariantMixin:
    def _apply_variant_style(self, hover: bool = False):
        """应用 variant 样式"""
        if self._variant == 'panel':
            theme = _get_theme(self)
            bg = theme.panel_bg_hover if hover else theme.panel_bg
            border = theme.panel_border_hover if hover else theme.panel_border
            self.setStyleSheet(f"""
                {self.__class__.__name__} {{
                    background-color: {bg};
                    border-radius: 12px;
                    padding: 12px;
                    border: 1px solid {border};
                }}
            """)
        elif self._variant == 'compact':
            self.setStyleSheet(f"{self.__class__.__name__} {{ border-radius: 6px; }}")
        else:
            self.setStyleSheet("")
    
    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件"""
        QWidget.enterEvent(self, event)
        if self._variant == 'panel':
            self._apply_variant_style(hover=True)
    
    def leaveEvent(self, event: QEvent):
        """鼠标离开事件"""
        QWidget.leaveEvent(self, event)
        if self._variant == 'panel':
            self._apply_variant_style(hover=False)


class Blocks(QWidget, _ContextMixin):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        theme: Optional[Union[str, Theme]] = None,
        visible: bool = True,
        elem_id: Optional[str] = None
    ):
        """初始化主容器"""
        super().__init__(parent)
        self._theme = Theme(theme) if isinstance(theme, str) else (theme or Theme('light'))
        
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        self._content_widget = QWidget()
        self._main_layout = QVBoxLayout(self._content_widget)
        self._main_layout.setContentsMargins(16, 16, 16, 16)
        self._main_layout.setSpacing(16)
        self._main_layout.addStretch()
        
        self._scroll_area.setWidget(self._content_widget)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._scroll_area)
        
        self._apply_theme()
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
    
    def _apply_theme(self):
        """应用主题样式"""
        bg = self._theme.background
        self.setStyleSheet(f"""
            Blocks {{ background-color: {bg}; }}
            QScrollArea {{ background-color: {bg}; border: none; }}
            QScrollArea > QWidget > QWidget {{ background-color: {bg}; }}
        """)
        self._content_widget.setStyleSheet(f"background-color: {bg};")
        self._update_children_theme()
    
    def _update_children_theme(self):
        """更新所有子组件的主题"""
        updated = set()
        for child in self.findChildren(QWidget):
            if child in updated:
                continue
            updated.add(child)
            if isinstance(child, (Row, Column)):
                child._apply_variant_style()
            elif isinstance(child, Button):
                child._apply_style()
            elif isinstance(child, ThemeToggleButton):
                child._update_button_appearance()
                child._apply_style()
    
    def toggle_theme(self):
        """切换主题"""
        self._theme = Theme('dark' if self._theme.mode == 'light' else 'light')
        self._apply_theme()
    
    def get_theme(self) -> Theme:
        """获取主题"""
        return self._theme
    
    def set_theme(self, theme: Union[str, Theme]):
        """设置主题"""
        self._theme = Theme(theme) if isinstance(theme, str) else theme
        self._apply_theme()
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._main_layout.removeItem(self._main_layout.itemAt(self._main_layout.count() - 1))
        self._main_layout.addWidget(widget)
        self._main_layout.addStretch()
    
    def launch(self, **kwargs):
        """启动（兼容接口）"""
        return self


class Row(QWidget, _ContextMixin, _VariantMixin):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        height: Optional[int] = None,
        max_height: Optional[int] = None,
        min_height: Optional[int] = None,
        equal_height: bool = False
    ):
        """初始化水平布局容器"""
        super().__init__(parent)
        self._variant = variant
        self._equal_height = equal_height
        
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0 if variant == 'compact' else 8)
        
        if elem_id:
            self.setObjectName(elem_id)
        if height:
            self.setFixedHeight(height)
        if max_height:
            self.setMaximumHeight(max_height)
        if min_height:
            self.setMinimumHeight(min_height)
        
        self._apply_variant_style()
        self.setVisible(visible)
        if variant == 'panel':
            self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget, stretch: int = 0):
        """添加子组件"""
        self._layout.addWidget(widget, stretch)
        if self._equal_height:
            widget.setMinimumHeight(self.height() if self.height() > 0 else 100)


class Column(QWidget, _ContextMixin, _VariantMixin):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        scale: int = 1,
        min_width: int = 320,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None
    ):
        """初始化垂直布局容器"""
        super().__init__(parent)
        self._scale = scale
        self._min_width = min_width
        self._variant = variant
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0 if variant == 'compact' else 8)
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setMinimumWidth(min_width)
        self._apply_variant_style()
        self.setVisible(visible)
        if variant == 'panel':
            self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._layout.addWidget(widget)
    
    def get_scale(self) -> int:
        """获取 scale 值"""
        return self._scale


class Group(QWidget, _ContextMixin):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        visible: bool = True,
        elem_id: Optional[str] = None
    ):
        """初始化分组容器"""
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._layout.addWidget(widget)


class Button(QPushButton):
    clicked_signal = pyqtSignal()
    
    def __init__(
        self,
        value: Union[str, Callable] = "Run",
        variant: Literal['primary', 'secondary', 'stop', 'huggingface'] = 'secondary',
        size: Literal['sm', 'md', 'lg'] = 'lg',
        icon: Optional[Union[str, Path]] = None,
        link: Optional[str] = None,
        visible: bool = True,
        interactive: bool = True,
        elem_id: Optional[str] = None,
        min_width: Optional[int] = None,
        parent: Optional[QWidget] = None
    ):
        """初始化按钮组件"""
        text = str(value() if callable(value) else value) if value else "Run"
        super().__init__(text, parent)
        self._value = text
        self._variant = variant
        self._size = size
        self._icon_path = icon
        self._link = link
        self._interactive = interactive
        
        if icon:
            self._set_icon(icon)
        if link:
            self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))
        else:
            self.clicked.connect(self._on_clicked)
        
        self._apply_style()
        if elem_id:
            self.setObjectName(elem_id)
        if min_width:
            self.setMinimumWidth(min_width)
        self.setEnabled(interactive)
        self.setVisible(visible)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if not parent:
            _auto_add_to_context(self)
    
    def _set_icon(self, icon: Union[str, Path]):
        """设置按钮图标"""
        try:
            icon_path = Path(icon) if isinstance(icon, str) else icon
            if icon_path.exists():
                self.setIcon(QIcon(str(icon_path)))
            else:
                self.setIcon(QIcon(str(icon)))
        except:
            pass
    
    def _apply_style(self):
        theme = _get_theme(self)
        size_styles = {
            'sm': "font-size: 12px; padding: 6px 12px; min-height: 28px;",
            'md': "font-size: 14px; padding: 8px 16px; min-height: 36px;",
            'lg': "font-size: 14px; padding: 12px 24px; min-height: 44px;"
        }
        
        if self._variant == 'primary':
            bg, hover, pressed, color, border = theme.primary, theme.primary_hover, theme.primary_pressed, "#FFFFFF", theme.primary
        elif self._variant == 'stop':
            bg, hover, pressed, color, border = theme.stop, theme.stop_hover, theme.stop_pressed, "#FFFFFF", theme.stop
        elif self._variant == 'huggingface':
            bg = "#000000" if theme.mode == 'light' else "#1F2937"
            hover = "#1F2937" if theme.mode == 'light' else "#2D2D2D"
            pressed = "#111827" if theme.mode == 'light' else "#1E1E1E"
            color, border = "#FFFFFF", bg
        else:
            bg, hover, pressed, color, border = theme.secondary, theme.secondary_hover, theme.secondary_pressed, theme.text, theme.secondary_border
        
        size_style = size_styles.get(self._size, size_styles['lg'])
        style = f"""
            QPushButton {{
                border-radius: 8px;
                font-weight: 500;
                {size_style}
                background-color: {bg};
                color: {color};
                border: 1px solid {border};
            }}
            QPushButton:hover {{ background-color: {hover}; border-color: {hover}; }}
            QPushButton:pressed {{ background-color: {pressed}; }}
            QPushButton:disabled {{ opacity: 0.5; }}
        """
        self.setStyleSheet(style)
    
    def _on_clicked(self):
        """点击事件处理"""
        self.clicked_signal.emit()
    
    def set_value(self, value: Union[str, Callable]):
        """设置按钮文本"""
        self._value = str(value() if callable(value) else value) if value else "Run"
        self.setText(self._value)
    
    def get_value(self) -> str:
        """获取按钮文本"""
        return self._value
    
    def set_variant(self, variant: Literal['primary', 'secondary', 'stop', 'huggingface']):
        """设置按钮样式变体"""
        self._variant = variant
        self._apply_style()
    
    def set_size(self, size: Literal['sm', 'md', 'lg']):
        """设置按钮尺寸"""
        self._size = size
        self._apply_style()
    
    def set_icon(self, icon: Union[str, Path]):
        """设置按钮图标"""
        self._icon_path = icon
        self._set_icon(icon)
    
    def set_link(self, link: Optional[str]):
        """设置按钮链接"""
        self._link = link
        self.clicked.disconnect()
        if link:
            self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))
        else:
            self.clicked.connect(self._on_clicked)
    
    def set_interactive(self, interactive: bool):
        """设置按钮交互状态"""
        self._interactive = interactive
        self.setEnabled(interactive)
    
    def click(self, fn: Optional[Callable] = None):
        """绑定点击回调"""
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal


class ThemeToggleButton(Button):
    def __init__(
        self,
        blocks: Optional['Blocks'] = None,
        parent: Optional[QWidget] = None,
        size: Literal['sm', 'md', 'lg'] = 'md',
        square: bool = True,
        visible: bool = True,
        interactive: bool = True
    ):
        """初始化主题切换按钮"""
        self._square = square
        super().__init__(
            value="",
            variant='secondary',
            size=size,
            visible=visible,
            interactive=interactive,
            parent=parent
        )
        
        if blocks:
            self._blocks = blocks
        else:
            current = self.parent()
            while current:
                if isinstance(current, Blocks):
                    self._blocks = current
                    break
                current = current.parent()
            else:
                raise ValueError("无法找到 Blocks 实例，请显式传入 blocks 参数")
        
        self.clicked_signal.connect(self._on_toggle_theme)
        self._update_button_appearance()
        self._apply_style()
    
    def _apply_style(self):
        """应用按钮样式（支持正方形外框）"""
        theme = _get_theme(self)
        size_configs = {
            'sm': {'font': '16px', 'padding': '4px', 'min_size': '32px'},
            'md': {'font': '20px', 'padding': '6px', 'min_size': '40px'},
            'lg': {'font': '24px', 'padding': '8px', 'min_size': '48px'}
        }
        cfg = size_configs.get(self._size, size_configs['md'])
        bg, hover, pressed, color, border = theme.secondary, theme.secondary_hover, theme.secondary_pressed, theme.text, theme.secondary_border
        
        square_style = f"""
            min-width: {cfg['min_size']};
            min-height: {cfg['min_size']};
            max-width: {cfg['min_size']};
            max-height: {cfg['min_size']};
        """ if self._square else ""
        
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 8px;
                font-weight: 500;
                font-size: {cfg['font']};
                padding: {cfg['padding']};
                background-color: {bg};
                color: {color};
                border: 1px solid {border};
                {square_style}
            }}
            QPushButton:hover {{ background-color: {hover}; border-color: {hover}; }}
            QPushButton:pressed {{ background-color: {pressed}; }}
            QPushButton:disabled {{ opacity: 0.5; }}
        """)
    
    def _update_button_appearance(self):
        """更新按钮外观"""
        theme = self._blocks.get_theme()
        if theme.mode == 'light':
            self.setText("🌙")
            self.setToolTip("切换到暗色主题")
        else:
            self.setText("☀️")
            self.setToolTip("切换到亮色主题")
    
    def _on_toggle_theme(self):
        """切换主题处理"""
        self._blocks.toggle_theme()
        self._update_button_appearance()
        self._apply_style()

