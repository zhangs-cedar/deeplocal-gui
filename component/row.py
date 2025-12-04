from typing import Union, Tuple
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import QTimer
from .context import _ContextMixin, _auto_add_to_context, _parse_margin_padding


class Row(QWidget, _ContextMixin):
    def __init__(self, parent=None,
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = 0):
        super().__init__(parent)
        margin_values = _parse_margin_padding(margin)
        padding_values = _parse_margin_padding(padding)
        self._margin = margin_values
        
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(*padding_values)
        self._layout.setSpacing(0)
        self._widgets = []
        self._relayout_timer = QTimer(self)
        self._relayout_timer.setSingleShot(True)
        self._relayout_timer.timeout.connect(self._do_relayout)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget, stretch: int = 0):
        # 添加 widget 并触发重新布局
        self._widgets.append(widget)
        self._schedule_relayout()
    
    def _schedule_relayout(self):
        # 延迟触发重新布局，避免频繁计算
        self._relayout_timer.start(10)
    
    def _do_relayout(self):
        if not self._widgets:
            return
        
        width = self.width()
        if width <= 0:
            return
        
        spacing = self._layout.spacing()
        margin = self._layout.contentsMargins()
        available = width - margin.left() - margin.right()
        min_w = 200
        cols = max(1, (available + spacing) // (min_w + spacing))
        
        if not hasattr(self, '_last_cols'):
            self._last_cols = 0
        
        if cols == self._last_cols and self._layout.count() == len(self._widgets):
            return
        
        self._last_cols = cols
        
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(None)
        
        for i, widget in enumerate(self._widgets):
            if widget.parent() != self:
                widget.setParent(self)
            self._layout.addWidget(widget, i // cols, i % cols)
    
    def _apply_style(self):
        from .theme import get_theme
        theme = get_theme()
        margin_css = f"margin: {' '.join(map(str, self._margin))}px;"
        self.setStyleSheet(f"QWidget {{ {margin_css} }}")
    
    def showEvent(self, event):
        super().showEvent(event)
        self._schedule_relayout()
        if hasattr(self, '_margin'):
            self._apply_style()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._schedule_relayout()
