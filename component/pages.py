from typing import Dict, Optional
from PyQt6.QtWidgets import QWidget, QStackedWidget
from .context import _ContextMixin, _auto_add_to_context


class Pages(QStackedWidget, _ContextMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pages: Dict[str, QWidget] = {}
        self._current_page: Optional[str] = None
        if not parent:
            _auto_add_to_context(self)
    
    def add_page(self, name: str, widget: QWidget):
        self._pages[name] = widget
        self.addWidget(widget)
        if not self._current_page:
            self.set_current_page(name)
    
    def set_current_page(self, name: str):
        if name in self._pages:
            self._current_page = name
            self.setCurrentWidget(self._pages[name])
    
    def get_current_page(self) -> Optional[str]:
        return self._current_page

