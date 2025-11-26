from typing import Optional, Literal, Callable, List, Union
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, 
    QScrollArea, QLayout, QLayoutItem, QWidgetItem
)
from PyQt6.QtCore import Qt, QEvent, pyqtSignal, QUrl, QSize, QRect, QPoint
from PyQt6.QtGui import QEnterEvent, QIcon, QDesktopServices

# 线程局部上下文栈（Linus 风格：避免全局状态，但保留 with 语句的便利性）
# 注意：在实际使用中，通常只有一个组件树，所以全局栈是安全的
# 如果需要在多个独立组件树中使用，可以考虑将栈作为 GradioBlocks 的实例属性
_context_stack: List[QWidget] = []


class GradioTheme:
    """Gradio 主题类"""
    
    def __init__(self, mode: Literal['light', 'dark'] = 'light'):
        """
        初始化主题
        
        Args:
            mode: 主题模式 ('light' 或 'dark')
        """
        self.mode = mode
        if mode == 'light':
            self._init_light_theme()
        else:
            self._init_dark_theme()
    
    def _init_light_theme(self):
        """初始化亮色主题"""
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
    
    def _init_dark_theme(self):
        """初始化暗色主题"""
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


def _get_theme(widget: QWidget) -> GradioTheme:
    """从组件树向上查找主题（直接调用，无全局状态）"""
    current = widget
    while current:
        if isinstance(current, GradioBlocks):
            return current._theme
        current = current.parent()
    return GradioTheme('light')  # 默认亮色主题


def _get_current_context() -> Optional[QWidget]:
    """
    获取当前上下文容器
    
    注意：使用模块级全局栈。在实际使用中通常只有一个组件树，这是安全的。
    如果需要支持多个独立的组件树，可以将栈作为 GradioBlocks 的实例属性。
    """
    return _context_stack[-1] if _context_stack else None


def _auto_add_to_context(widget: QWidget):
    """自动将组件添加到当前上下文（Linus 风格：直接调用）"""
    if widget.parent():
        return
    
    current = _get_current_context()
    if not current:
        return
    
    # 直接调用父组件方法，无间接调用
    if isinstance(current, GradioTabs) and isinstance(widget, GradioTab):
        current.addTab(widget)
    elif isinstance(current, GradioTab):
        current.addWidget(widget)
    elif isinstance(current, GradioRow):
        stretch = widget.get_scale() if isinstance(widget, GradioColumn) else 0
        current.addWidget(widget, stretch)
    elif isinstance(current, (GradioColumn, GradioGroup, GradioBlocks, GradioFlow)):
        current.addWidget(widget)


class _ContextMixin:
    """上下文管理器混入类"""
    def __enter__(self):
        _context_stack.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False


class _VariantMixin:
    """Variant 样式混入类"""
    def _apply_variant_style(self, hover: bool = False):
        """应用 variant 样式（Linus 风格：直接、简洁）"""
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


class GradioBlocks(QWidget, _ContextMixin):
    """
    Gradio 风格的 Blocks 容器组件
    参考 Gradio Blocks: https://www.gradio.app/docs/gradio/blocks
    主容器，支持 with 语句和上下文管理，自动支持滚动
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        theme: Optional[Union[str, GradioTheme]] = None,
        title: Optional[str] = None,
        visible: bool = True,
        elem_id: Optional[str] = None
    ):
        super().__init__(parent)
        
        # 设置主题
        if theme is None:
            self._theme = GradioTheme('light')  # 默认亮色主题
        elif isinstance(theme, str):
            self._theme = GradioTheme(theme)
        else:
            self._theme = theme
        
        # 创建滚动区域
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # 创建内容容器
        self._content_widget = QWidget()
        self._main_layout = QVBoxLayout(self._content_widget)
        self._main_layout.setContentsMargins(16, 16, 16, 16)
        self._main_layout.setSpacing(16)
        self._main_layout.addStretch()
        
        self._scroll_area.setWidget(self._content_widget)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._scroll_area)
        
        # 应用主题样式
        self._apply_theme()
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
    
    def _apply_theme(self):
        """应用主题样式"""
        self.setStyleSheet(f"""
            GradioBlocks {{
                background-color: {self._theme.background};
            }}
            QScrollArea {{
                background-color: {self._theme.background};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {self._theme.background};
            }}
        """)
        # 直接设置内容容器的背景色
        if hasattr(self, '_content_widget'):
            self._content_widget.setStyleSheet(f"background-color: {self._theme.background};")
        
        # 通知所有子组件更新主题
        self._update_children_theme()
    
    def _update_children_theme(self):
        """更新所有子组件的主题（直接调用）"""
        updated = set()
        
        def update_widget(widget):
            if widget in updated:
                return
            updated.add(widget)
            
            # 直接调用组件方法，无间接调用
            if isinstance(widget, GradioTabs):
                widget._apply_theme()
            elif isinstance(widget, (GradioRow, GradioColumn, GradioFlow)):
                widget._apply_variant_style()
            elif isinstance(widget, GradioButton):
                widget._apply_style()
            elif isinstance(widget, GradioThemeToggleButton):
                widget._update_button_appearance()
                widget._apply_style()
        
        for child in self.findChildren(QWidget):
            update_widget(child)
    
    def toggle_theme(self):
        """切换主题（Linus 风格：直接、简洁）"""
        self._theme = GradioTheme('dark' if self._theme.mode == 'light' else 'light')
        self._apply_theme()
    
    def get_theme(self) -> GradioTheme:
        """获取当前主题"""
        return self._theme
    
    def set_theme(self, theme: Union[str, GradioTheme]):
        """设置主题（Linus 风格：直接调用）"""
        self._theme = GradioTheme(theme) if isinstance(theme, str) else theme
        self._apply_theme()
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._main_layout.removeItem(self._main_layout.itemAt(self._main_layout.count() - 1))
        self._main_layout.addWidget(widget)
        self._main_layout.addStretch()
    
    def launch(self, **kwargs):
        """启动应用（兼容 Gradio API）"""
        return self


class GradioRow(QWidget, _ContextMixin, _VariantMixin):
    """
    Gradio 风格的 Row 组件 - 水平布局容器
    参考 Gradio Row: https://www.gradio.app/docs/gradio/row
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None,
        scale: Optional[int] = None,
        height: Optional[int] = None,
        max_height: Optional[int] = None,
        min_height: Optional[int] = None,
        equal_height: bool = False,
        show_progress: bool = False
    ):
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


class GradioColumn(QWidget, _ContextMixin, _VariantMixin):
    """
    Gradio 风格的 Column 组件 - 垂直布局容器
    参考 Gradio Column: https://www.gradio.app/docs/gradio/column
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        scale: int = 1,
        min_width: int = 320,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None,
        show_progress: bool = False
    ):
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
    
    def get_min_width(self) -> int:
        """获取 min_width 值"""
        return self._min_width


class GradioGroup(QWidget, _ContextMixin):
    """
    Gradio 风格的 Group 组件 - 分组容器
    参考 Gradio Group: https://www.gradio.app/docs/gradio/group
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None
    ):
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


class GradioTabs(QWidget, _ContextMixin):
    """
    Gradio 风格的 Tabs 容器组件
    参考 Gradio Tab: https://www.gradio.app/docs/gradio/tab
    """
    
    tab_selected = pyqtSignal(str, bool)
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None
    ):
        super().__init__(parent)
        
        self._tabs: List['GradioTab'] = []
        self._current_index = 0
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab 按钮栏
        self._button_bar = QWidget()
        self._button_layout = QHBoxLayout(self._button_bar)
        self._button_layout.setContentsMargins(0, 0, 0, 0)
        self._button_layout.setSpacing(0)
        layout.addWidget(self._button_bar)
        
        # 内容区域
        self._stacked_widget = QStackedWidget()
        layout.addWidget(self._stacked_widget)
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
        
        if not parent:
            _auto_add_to_context(self)
            # 添加到上下文后应用主题
            self._apply_theme()
    
    def _apply_theme(self):
        """应用主题样式"""
        theme = _get_theme(self)
        self._button_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.tab_bg};
                border-bottom: 1px solid {theme.border};
            }}
        """)
        self._stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {theme.background};
            }}
        """)
    
    def addTab(self, tab: 'GradioTab'):
        """添加 Tab"""
        self._tabs.append(tab)
        tab.setParent(self)
        
        # 创建 Tab 按钮
        button = QPushButton(tab.get_label() or f"Tab {len(self._tabs)}")
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda checked, idx=len(self._tabs)-1: self._on_tab_clicked(idx))
        
        # 应用按钮样式
        self._apply_button_style(button, len(self._tabs) - 1 == self._current_index)
        self._button_layout.addWidget(button)
        tab._button = button
        
        # 添加内容到 StackedWidget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(8)
        tab._content_widget = content_widget
        
        # 将 Tab 布局中的组件移动到内容区域
        while tab._layout.count():
            item = tab._layout.takeAt(0)
            if item.widget():
                content_layout.addWidget(item.widget())
        
        self._stacked_widget.addWidget(content_widget)
        
        # 如果是第一个 Tab，设置为选中
        if len(self._tabs) == 1:
            self._set_current_tab(0)
    
    def _on_tab_clicked(self, index: int):
        """Tab 按钮点击事件"""
        if 0 <= index < len(self._tabs):
            tab = self._tabs[index]
            if tab.is_interactive():
                self._set_current_tab(index)
                self.tab_selected.emit(tab.get_label() or "", True)
    
    def _set_current_tab(self, index: int):
        """设置当前选中的 Tab"""
        if 0 <= index < len(self._tabs):
            self._current_index = index
            self._stacked_widget.setCurrentIndex(index)
            
            # 更新所有按钮样式
            for i, tab in enumerate(self._tabs):
                if tab._button:
                    self._apply_button_style(tab._button, i == index)
    
    def _apply_button_style(self, button: QPushButton, selected: bool):
        """应用按钮样式"""
        theme = _get_theme(self)
        if selected:
            style = f"""
                QPushButton {{
                    background-color: {theme.tab_selected_bg};
                    color: {theme.tab_text_selected};
                    border: none;
                    border-bottom: 2px solid {theme.tab_border};
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {theme.background_secondary};
                }}
            """
            button.setChecked(True)
        else:
            style = f"""
                QPushButton {{
                    background-color: transparent;
                    color: {theme.tab_text};
                    border: none;
                    border-bottom: 2px solid transparent;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 400;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {theme.background_tertiary};
                    color: {theme.tab_text_selected};
                }}
            """
            button.setChecked(False)
        button.setStyleSheet(style)
    
    def get_current_index(self) -> int:
        """获取当前选中的 Tab 索引"""
        return self._current_index
    
    def set_current_index(self, index: int):
        """设置当前选中的 Tab 索引"""
        self._set_current_tab(index)


class GradioTab(QWidget, _ContextMixin):
    """
    Gradio 风格的 Tab 组件
    参考 Gradio Tab: https://www.gradio.app/docs/gradio/tab
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        label: Optional[str] = None,
        visible: bool = True,
        interactive: bool = True,
        tab_id: Optional[str] = None,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None,
        scale: Optional[int] = None,
        render_children: bool = False
    ):
        super().__init__(parent)
        
        self._label = label
        self._interactive = interactive
        self._tab_id = tab_id
        self._button: Optional[QPushButton] = None
        self._content_widget: Optional[QWidget] = None
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
    
    def addWidget(self, widget: QWidget):
        """添加子组件到 Tab 内容区域"""
        if self._content_widget:
            layout = self._content_widget.layout()
            if layout:
                layout.addWidget(widget)
        else:
            # 如果还没有添加到 Tabs 容器，先添加到自己的布局
            # 稍后当 Tab 被添加到 Tabs 容器时，这些组件会被移动到内容区域
            self._layout.addWidget(widget)
    
    def get_label(self) -> Optional[str]:
        """获取 Tab 标签"""
        return self._label
    
    def set_label(self, label: str):
        """设置 Tab 标签"""
        self._label = label
        if self._button:
            self._button.setText(label)
    
    def is_interactive(self) -> bool:
        """是否可交互"""
        return self._interactive
    
    def set_interactive(self, interactive: bool):
        """设置是否可交互"""
        self._interactive = interactive
        if self._button:
            self._button.setEnabled(interactive)
    
    def get_tab_id(self) -> Optional[str]:
        """获取 Tab ID"""
        return self._tab_id


class GradioButton(QPushButton):
    """
    Gradio 风格的 Button 组件
    参考 Gradio Button: https://www.gradio.app/docs/gradio/button
    支持多种样式变体、大小、图标和链接
    """
    
    clicked_signal = pyqtSignal()  # 点击信号
    
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
        elem_classes: Optional[str] = None,
        scale: Optional[int] = None,
        min_width: Optional[int] = None,
        parent: Optional[QWidget] = None
    ):
        """
        初始化 Button 组件
        
        Args:
            value: 按钮显示的文本，默认 "Run"
            variant: 按钮样式变体 ('primary', 'secondary', 'stop', 'huggingface')
            size: 按钮大小 ('sm', 'md', 'lg')
            icon: 图标路径或 URL
            link: 点击时打开的链接 URL
            visible: 是否可见
            interactive: 是否可交互
            elem_id: HTML DOM id（PyQt6 中作为 objectName）
            elem_classes: HTML DOM class（PyQt6 中用于样式）
            scale: 相对大小（未实现）
            min_width: 最小宽度（像素）
            parent: 父组件
        """
        # 处理 value 可能是函数的情况
        if callable(value):
            text = str(value()) if value else "Run"
        else:
            text = str(value) if value else "Run"
        
        super().__init__(text, parent)
        
        self._value = text
        self._variant = variant
        self._size = size
        self._icon_path = icon
        self._link = link
        self._interactive = interactive
        
        # 设置图标
        if icon:
            self._set_icon(icon)
        
        # 设置链接
        if link:
            self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))
        else:
            self.clicked.connect(self._on_clicked)
        
        # 设置样式
        self._apply_style()
        
        # 设置属性
        if elem_id:
            self.setObjectName(elem_id)
        
        if min_width:
            self.setMinimumWidth(min_width)
        
        self.setEnabled(interactive)
        self.setVisible(visible)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 自动添加到当前上下文（如果没有指定 parent）
        if not parent:
            _auto_add_to_context(self)
    
    def _set_icon(self, icon: Union[str, Path]):
        """设置按钮图标"""
        try:
            icon_path = Path(icon) if isinstance(icon, str) else icon
            if icon_path.exists():
                self.setIcon(QIcon(str(icon_path)))
            else:
                # 如果是 URL 或其他格式，尝试直接使用
                self.setIcon(QIcon(str(icon)))
        except:
            pass
    
    def _apply_style(self):
        """应用按钮样式"""
        theme = _get_theme(self)
        size_styles = {
            'sm': "font-size: 12px; padding: 6px 12px; min-height: 28px;",
            'md': "font-size: 14px; padding: 8px 16px; min-height: 36px;",
            'lg': "font-size: 14px; padding: 12px 24px; min-height: 44px;"
        }
        
        # 根据 variant 选择主题颜色
        if self._variant == 'primary':
            bg = theme.primary
            hover = theme.primary_hover
            pressed = theme.primary_pressed
            color = "#FFFFFF"
            border = theme.primary
        elif self._variant == 'stop':
            bg = theme.stop
            hover = theme.stop_hover
            pressed = theme.stop_pressed
            color = "#FFFFFF"
            border = theme.stop
        elif self._variant == 'huggingface':
            bg = "#000000" if theme.mode == 'light' else "#1F2937"
            hover = "#1F2937" if theme.mode == 'light' else "#2D2D2D"
            pressed = "#111827" if theme.mode == 'light' else "#1E1E1E"
            color = "#FFFFFF"
            border = bg
        else:  # secondary
            bg = theme.secondary
            hover = theme.secondary_hover
            pressed = theme.secondary_pressed
            color = theme.text
            border = theme.secondary_border
        
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
            QPushButton:hover {{
                background-color: {hover};
                border-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """
        self.setStyleSheet(style)
    
    def _on_clicked(self):
        """按钮点击事件"""
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
        """设置按钮大小"""
        self._size = size
        self._apply_style()
    
    def set_icon(self, icon: Union[str, Path]):
        """设置按钮图标"""
        self._icon_path = icon
        self._set_icon(icon)
    
    def set_link(self, link: Optional[str]):
        """设置链接"""
        self._link = link
        # 断开之前的连接
        self.clicked.disconnect()
        if link:
            self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))
        else:
            self.clicked.connect(self._on_clicked)
    
    def set_interactive(self, interactive: bool):
        """设置是否可交互"""
        self._interactive = interactive
        self.setEnabled(interactive)
    
    def click(self, fn: Optional[Callable] = None):
        """
        设置点击事件监听器
        
        Args:
            fn: 点击时调用的函数
        
        Returns:
            如果提供了函数，返回信号连接；否则返回信号本身
        """
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal


class GradioFlowLayout(QLayout):
    """
    流式布局 - 支持自动换行的布局
    类似于 CSS flexbox 的 wrap 效果
    """
    
    def __init__(self, parent: Optional[QWidget] = None, spacing: int = 8):
        super().__init__(parent)
        self._items: List[QLayoutItem] = []
        self._spacing = spacing
        self._horizontal_spacing = spacing
        self._vertical_spacing = spacing
    
    def addItem(self, item: QLayoutItem):
        """添加布局项"""
        self._items.append(item)
    
    def addWidget(self, widget: QWidget):
        """添加组件"""
        self.addItem(QWidgetItem(widget))
    
    def count(self) -> int:
        """返回布局项数量"""
        return len(self._items)
    
    def itemAt(self, index: int) -> Optional[QLayoutItem]:
        """获取指定索引的布局项"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None
    
    def takeAt(self, index: int) -> Optional[QLayoutItem]:
        """移除并返回指定索引的布局项"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None
    
    def setSpacing(self, spacing: int):
        """设置间距"""
        self._spacing = spacing
        self._horizontal_spacing = spacing
        self._vertical_spacing = spacing
    
    def spacing(self) -> int:
        """获取间距"""
        return self._spacing
    
    def expandingDirections(self) -> Qt.Orientation:
        """返回布局的扩展方向"""
        return Qt.Orientation(0)
    
    def hasHeightForWidth(self) -> bool:
        """是否支持根据宽度计算高度"""
        return True
    
    def heightForWidth(self, width: int) -> int:
        """根据宽度计算高度"""
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)
    
    def sizeHint(self) -> QSize:
        """返回布局的推荐大小"""
        return self.minimumSize()
    
    def minimumSize(self) -> QSize:
        """返回布局的最小大小"""
        size = QSize()
        
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size
    
    def setGeometry(self, rect: QRect):
        """设置布局的几何形状"""
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)
    
    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        """执行布局计算"""
        if not self._items:
            return 0
        
        margins = self.contentsMargins()
        effective_rect = rect.adjusted(
            margins.left(), margins.top(),
            -margins.right(), -margins.bottom()
        )
        
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0
        space_x = self._horizontal_spacing
        space_y = self._vertical_spacing
        
        for item in self._items:
            widget = item.widget()
            if widget and not widget.isVisible():
                continue
            
            item_size = item.sizeHint()
            item_width = item_size.width()
            item_height = item_size.height()
            
            # 检查是否需要换行（如果当前行已经有内容，且加上这个项目会超出边界）
            if x > effective_rect.x() and x + item_width > effective_rect.right():
                # 需要换行
                x = effective_rect.x()
                y = y + line_height + space_y
                line_height = 0
            
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_size))
            
            x = x + item_width + space_x
            line_height = max(line_height, item_height)
        
        return y + line_height - rect.y() + margins.bottom()


class GradioFlow(QWidget, _ContextMixin, _VariantMixin):
    """
    Gradio 风格的流式布局容器
    支持自动换行，类似于 CSS flexbox 的 wrap 效果
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        spacing: int = 8,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None
    ):
        super().__init__(parent)
        
        self._variant = variant
        self._spacing = spacing
        
        # 使用流式布局
        self._layout = GradioFlowLayout(self, spacing=spacing if variant != 'compact' else 0)
        self.setLayout(self._layout)
        
        if elem_id:
            self.setObjectName(elem_id)
        
        self._apply_variant_style()
        self.setVisible(visible)
        
        if variant == 'panel':
            self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._layout.addWidget(widget)
    
    def setSpacing(self, spacing: int):
        """设置间距"""
        self._spacing = spacing
        self._layout.setSpacing(spacing)
    
    def getSpacing(self) -> int:
        """获取间距"""
        return self._spacing


class GradioThemeToggleButton(GradioButton):
    """
    主题切换按钮
    根据当前主题显示月亮（亮色）或太阳（暗色）图标
    支持配置正方形外框
    """
    
    def __init__(
        self,
        blocks: Optional['GradioBlocks'] = None,
        parent: Optional[QWidget] = None,
        size: Literal['sm', 'md', 'lg'] = 'md',
        square: bool = True,
        visible: bool = True,
        interactive: bool = True
    ):
        """
        初始化主题切换按钮
        
        Args:
            blocks: GradioBlocks 实例，如果为 None 则自动查找
            parent: 父组件
            size: 按钮大小
            square: 是否使用正方形外框（默认 True）
            visible: 是否可见
            interactive: 是否可交互
        """
        # 先设置 _square 属性，因为父类 __init__ 会调用 _apply_style
        self._square = square
        
        # 先创建按钮，稍后设置图标和文本
        super().__init__(
            value="",
            variant='secondary',
            size=size,
            visible=visible,
            interactive=interactive,
            parent=parent
        )
        
        # 查找或设置 Blocks
        if blocks:
            self._blocks = blocks
        else:
            # 向上查找 GradioBlocks
            current = self.parent()
            while current:
                if isinstance(current, GradioBlocks):
                    self._blocks = current
                    break
                current = current.parent()
            else:
                raise ValueError("无法找到 GradioBlocks 实例，请显式传入 blocks 参数")
        
        # 连接切换主题的信号
        self.clicked_signal.connect(self._on_toggle_theme)
        
        # 更新按钮图标和文本
        self._update_button_appearance()
        
        # 应用样式（包括正方形配置）
        self._apply_style()
        
        # Linus 风格：直接引用，无需监听机制
    
    def _apply_style(self):
        """重写样式应用，支持正方形外框配置"""
        theme = _get_theme(self)
        size_styles = {
            'sm': {
                'font': '16px',
                'padding': '4px',
                'min_size': '32px'
            },
            'md': {
                'font': '20px',
                'padding': '6px',
                'min_size': '40px'
            },
            'lg': {
                'font': '24px',
                'padding': '8px',
                'min_size': '48px'
            }
        }
        
        size_config = size_styles.get(self._size, size_styles['md'])
        
        # 使用 secondary 变体的颜色
        bg = theme.secondary
        hover = theme.secondary_hover
        pressed = theme.secondary_pressed
        color = theme.text
        border = theme.secondary_border
        
        # 如果启用正方形，设置最小宽度和高度相等
        # 检查 _square 属性是否存在（兼容父类调用时的情况）
        if hasattr(self, '_square') and self._square:
            square_style = f"""
                min-width: {size_config['min_size']};
                min-height: {size_config['min_size']};
                max-width: {size_config['min_size']};
                max-height: {size_config['min_size']};
            """
        else:
            square_style = ""
        
        style = f"""
            QPushButton {{
                border-radius: 8px;
                font-weight: 500;
                font-size: {size_config['font']};
                padding: {size_config['padding']};
                background-color: {bg};
                color: {color};
                border: 1px solid {border};
                {square_style}
            }}
            QPushButton:hover {{
                background-color: {hover};
                border-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """
        self.setStyleSheet(style)
    
    def _update_button_appearance(self):
        """更新按钮外观（图标和文本）"""
        theme = self._blocks.get_theme()
        if theme.mode == 'light':
            # 亮色主题：显示月亮图标（切换到暗色）
            self.setText("🌙")
            self.setToolTip("切换到暗色主题")
        else:
            # 暗色主题：显示太阳图标（切换到亮色）
            self.setText("☀️")
            self.setToolTip("切换到亮色主题")
    
    def _on_toggle_theme(self):
        """切换主题"""
        self._blocks.toggle_theme()
        self._update_button_appearance()
        # 更新按钮样式以匹配新主题
        self._apply_style()

