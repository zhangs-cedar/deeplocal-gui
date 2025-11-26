from typing import Dict, Optional, Callable, Union
from PyQt6.QtWidgets import QWidget, QStackedWidget
from .context import _ContextMixin, _auto_add_to_context


class Pages(QStackedWidget, _ContextMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 存储页面工厂函数（用于延迟加载）
        self._page_factories: Dict[str, Callable[[], QWidget]] = {}
        # 存储直接传入的 widget（向后兼容）
        self._direct_widgets: Dict[str, QWidget] = {}
        self._current_page: Optional[str] = None
        if not parent:
            _auto_add_to_context(self)
    
    def add_page(self, name: str, widget_or_factory: Union[QWidget, Callable[[], QWidget]]):
        """
        添加页面，支持两种方式：
        1. 直接传入 widget：立即添加到 QStackedWidget（向后兼容）
        2. 传入工厂函数：延迟加载，每次切换时重新创建
        """
        if callable(widget_or_factory) and not isinstance(widget_or_factory, QWidget):
            # 工厂函数模式：延迟加载，每次切换时重新创建
            self._page_factories[name] = widget_or_factory
        else:
            # 直接传入 widget：立即添加（向后兼容）
            widget = widget_or_factory
            self._direct_widgets[name] = widget
            self.addWidget(widget)
            if not self._current_page:
                self.set_current_page(name)
    
    def _destroy_current_page(self):
        """销毁当前页面"""
        if self._current_page:
            # 获取当前显示的 widget
            current_widget = self.currentWidget()
            if current_widget:
                # 从 QStackedWidget 中移除
                self.removeWidget(current_widget)
                # 销毁 widget
                current_widget.deleteLater()
    
    def set_current_page(self, name: str):
        """
        切换到指定页面，每次切换时：
        1. 销毁上一个页面
        2. 重新创建新页面（如果是工厂函数模式）
        """
        # 如果切换到同一个页面，不处理
        if self._current_page == name:
            return
        
        # 销毁当前页面
        self._destroy_current_page()
        
        # 创建并切换到新页面
        if name in self._page_factories:
            # 工厂函数模式：每次切换都重新创建
            factory = self._page_factories[name]
            widget = factory()
            self.addWidget(widget)
            self.setCurrentWidget(widget)
            self._current_page = name
        elif name in self._direct_widgets:
            # 直接传入的 widget 模式：直接切换
            widget = self._direct_widgets[name]
            self.setCurrentWidget(widget)
            self._current_page = name
    
    def get_current_page(self) -> Optional[str]:
        return self._current_page

