"""
Gradio 风格的卡片组件
支持 header、body、footer 三个区域，以及阴影效果
参考 Gradio 组件风格实现
"""
from typing import Optional, Literal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QEnterEvent, QColor

# 使用相对导入避免模块路径问题
try:
    from .gradio import _ContextMixin, _get_theme, _auto_add_to_context, GradioTheme
except ImportError:
    # 如果相对导入失败，尝试绝对导入（用于直接运行文件时）
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from component.gradio import _ContextMixin, _get_theme, _auto_add_to_context, GradioTheme


class GradioCard(QWidget, _ContextMixin):
    """
    Gradio 风格的卡片组件
    参考 Gradio 组件风格，支持主题、上下文管理等
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        shadow: Literal['always', 'hover', 'never'] = 'always',
        body_style: Optional[str] = None,
        header_class: Optional[str] = None,
        body_class: Optional[str] = None,
        footer_class: Optional[str] = None,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None
    ):
        super().__init__(parent)
        
        self._shadow = shadow
        self._body_style = body_style or ""
        self._header_class = header_class or ""
        self._body_class = body_class or ""
        self._footer_class = footer_class or ""
        
        self._header_widget: Optional[QWidget] = None
        self._body_widget: Optional[QWidget] = None
        self._footer_widget: Optional[QWidget] = None
        
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        
        self._shadow_effect: Optional[QGraphicsDropShadowEffect] = None
        self._init_ui(header, footer)
        self._update_shadow()
        
        if elem_id:
            self.setObjectName(elem_id)
        self.setVisible(visible)
        
        if not parent:
            _auto_add_to_context(self)
    
    def _init_ui(self, header: Optional[str], footer: Optional[str]):
        """初始化UI"""
        if header:
            self._header_widget = QLabel(header)
            self._header_widget.setObjectName("card_header")
            self._header_widget.setStyleSheet(self._get_header_style())
            self._main_layout.addWidget(self._header_widget)
        
        self._body_widget = QWidget()
        self._body_widget.setObjectName("card_body")
        self._body_layout = QVBoxLayout(self._body_widget)
        self._body_layout.setContentsMargins(20, 20, 20, 20)
        self._body_layout.setSpacing(0)
        
        if self._body_style:
            self._body_widget.setStyleSheet(self._body_style)
        else:
            self._body_widget.setStyleSheet(self._get_body_style())
        
        self._main_layout.addWidget(self._body_widget)
        
        if footer:
            self._footer_widget = QLabel(footer)
            self._footer_widget.setObjectName("card_footer")
            self._footer_widget.setStyleSheet(self._get_footer_style())
            self._main_layout.addWidget(self._footer_widget)
        
        self.setStyleSheet(self._get_card_base_style())
    
    def _is_dark_theme(self) -> bool:
        """检测当前是否为深色主题"""
        theme = _get_theme(self)
        return theme.mode == 'dark'
    
    def _get_card_base_style(self, hover: bool = False) -> str:
        """获取卡片基础样式"""
        theme = _get_theme(self)
        if hover:
            return f"""
                GradioCard {{
                    background-color: {theme.background};
                    border: 2px solid {theme.primary};
                    border-radius: 8px;
                }}
            """
        else:
            return f"""
                GradioCard {{
                    background-color: {theme.background};
                    border: 1px solid {theme.border};
                    border-radius: 8px;
                }}
            """
    
    def _get_header_style(self) -> str:
        """获取 header 样式"""
        theme = _get_theme(self)
        return f"""
            padding: 16px 20px;
            border-bottom: 1px solid {theme.border};
            font-size: 16px;
            font-weight: 500;
            color: {theme.text};
            background-color: {theme.background};
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """
    
    def _get_body_style(self) -> str:
        """获取 body 样式"""
        theme = _get_theme(self)
        return f"""
            background-color: {theme.background};
            color: {theme.text_secondary};
            font-size: 14px;
        """
    
    def _get_footer_style(self) -> str:
        """获取 footer 样式"""
        theme = _get_theme(self)
        return f"""
            padding: 16px 20px;
            border-top: 1px solid {theme.border};
            font-size: 14px;
            color: {theme.text_secondary};
            background-color: {theme.background};
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        """
    
    def _update_shadow(self):
        """更新阴影效果"""
        if self._shadow_effect:
            self.setGraphicsEffect(None)
            self._shadow_effect = None
        
        if self._shadow == 'always':
            self._apply_shadow()
        
        self.setStyleSheet(self._get_card_base_style())
    
    def _apply_shadow(self):
        """应用阴影效果"""
        if not self._shadow_effect:
            self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setBlurRadius(12)
            self._shadow_effect.setXOffset(0)
            self._shadow_effect.setYOffset(2)
            
            if self._is_dark_theme():
                theme = _get_theme(self)
                # 使用主题的主色调作为阴影
                self._shadow_effect.setColor(QColor(99, 102, 241, 100))  # primary color with alpha
            else:
                self._shadow_effect.setColor(QColor(0, 0, 0, 50))
        
        try:
            self.setGraphicsEffect(self._shadow_effect)
        except RuntimeError:
            self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setBlurRadius(12)
            self._shadow_effect.setXOffset(0)
            self._shadow_effect.setYOffset(2)
            if self._is_dark_theme():
                self._shadow_effect.setColor(QColor(99, 102, 241, 100))
            else:
                self._shadow_effect.setColor(QColor(0, 0, 0, 50))
            self.setGraphicsEffect(self._shadow_effect)
    
    def _remove_shadow(self):
        """移除阴影效果"""
        try:
            if self._shadow_effect:
                self.setGraphicsEffect(None)
        except RuntimeError:
            self._shadow_effect = None
    
    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件"""
        super().enterEvent(event)
        if self._shadow == 'hover':
            self._apply_shadow()
        self.setStyleSheet(self._get_card_base_style(hover=True))
    
    def leaveEvent(self, event: QEvent):
        """鼠标离开事件"""
        super().leaveEvent(event)
        if self._shadow == 'hover':
            self._remove_shadow()
        self.setStyleSheet(self._get_card_base_style(hover=False))
    
    def setHeaderWidget(self, widget: QWidget):
        """设置自定义 header 组件"""
        if self._header_widget:
            self._main_layout.removeWidget(self._header_widget)
            self._header_widget.setParent(None)
        
        self._header_widget = widget
        if widget:
            widget.setObjectName("card_header")
            widget.setStyleSheet(self._get_header_style())
            self._main_layout.insertWidget(0, widget)
    
    def setFooterWidget(self, widget: QWidget):
        """设置自定义 footer 组件"""
        if self._footer_widget:
            self._main_layout.removeWidget(self._footer_widget)
            self._footer_widget.setParent(None)
        
        self._footer_widget = widget
        if widget:
            widget.setObjectName("card_footer")
            widget.setStyleSheet(self._get_footer_style())
            self._main_layout.addWidget(widget)
    
    def addWidget(self, widget: QWidget):
        """添加内容到 body 区域（兼容 Gradio API）"""
        self._body_layout.addWidget(widget)
    
    def setBodyStyle(self, style: str):
        """设置 body 样式"""
        self._body_style = style
        if self._body_widget:
            self._body_widget.setStyleSheet(style)
    
    def setShadow(self, shadow: Literal['always', 'hover', 'never']):
        """设置阴影效果"""
        valid_shadows = ['always', 'hover', 'never']
        if shadow in valid_shadows:
            self._shadow = shadow
            self._update_shadow()
    
    def getHeaderWidget(self) -> Optional[QWidget]:
        """获取 header 组件"""
        return self._header_widget
    
    def getBodyWidget(self) -> QWidget:
        """获取 body 组件"""
        return self._body_widget
    
    def getFooterWidget(self) -> Optional[QWidget]:
        """获取 footer 组件"""
        return self._footer_widget


# 为了向后兼容，保留 Card 作为 GradioCard 的别名
Card = GradioCard

