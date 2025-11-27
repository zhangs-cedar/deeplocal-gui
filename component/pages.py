from typing import Dict, Optional, Callable, Union
from PyQt6.QtWidgets import QWidget, QStackedWidget
from PyQt6.QtCore import QTimer
from .context import _ContextMixin, _auto_add_to_context


class Pages(QStackedWidget, _ContextMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._page_factories: Dict[str, Callable[[], QWidget]] = {}
        self._direct_widgets: Dict[str, QWidget] = {}
        self._current_page: Optional[str] = None
        if not parent:
            _auto_add_to_context(self)
    
    def add_page(self, name: str, widget_or_factory: Union[QWidget, Callable[[], QWidget]]):
        if callable(widget_or_factory) and not isinstance(widget_or_factory, QWidget):
            self._page_factories[name] = widget_or_factory
        else:
            widget = widget_or_factory
            self._direct_widgets[name] = widget
            self.addWidget(widget)
            if not self._current_page:
                self.set_current_page(name)
    
    def _apply_theme_to_widgets(self, widget: QWidget):
        """递归应用主题到所有子组件"""
        if hasattr(widget, '_apply_style'):
            widget._apply_style()
        
        # 处理 Row 的 _widgets 列表
        if hasattr(widget, '_widgets'):
            for child in widget._widgets:
                self._apply_theme_to_widgets(child)
        
        # 递归处理所有子组件
        for child in widget.findChildren(QWidget):
            if hasattr(child, '_apply_style'):
                child._apply_style()
    
    def _destroy_current_page(self):
        if self._current_page:
            current_widget = self.currentWidget()
            if current_widget:
                self.removeWidget(current_widget)
                current_widget.deleteLater()
    
    def set_current_page(self, name: str):
        if self._current_page == name:
            return
        
        self._destroy_current_page()
        
        if name in self._page_factories:
            widget = self._page_factories[name]()
            widget.setVisible(False)
            self.addWidget(widget)
            self.setCurrentWidget(widget)
            self._current_page = name
            # 延迟应用主题，确保 widget 树已建立
            QTimer.singleShot(0, lambda: (self._apply_theme_to_widgets(widget), widget.setVisible(True)))
        elif name in self._direct_widgets:
            widget = self._direct_widgets[name]
            widget.setVisible(False)
            self.setCurrentWidget(widget)
            self._current_page = name
            QTimer.singleShot(0, lambda: (self._apply_theme_to_widgets(widget), widget.setVisible(True)))
    
    def get_current_page(self) -> Optional[str]:
        return self._current_page

