from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import QTimer
from .context import _ContextMixin, _auto_add_to_context


class Row(QWidget, _ContextMixin):
    def __init__(self, parent=None):
        # 初始化响应式横向布局容器
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(16)
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
        # 根据窗口宽度计算列数并重新排列 widget
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(None)
        if not self._widgets:
            return
        
        width = self.width()
        if width <= 0:
            width = 400
        
        spacing = self._layout.spacing()
        margin = self._layout.contentsMargins()
        available = width - margin.left() - margin.right()
        min_w = 200
        cols = max(1, (available + spacing) // (min_w + spacing))
        
        for i, widget in enumerate(self._widgets):
            if widget.parent() != self:
                widget.setParent(self)
            self._layout.addWidget(widget, i // cols, i % cols)
    
    def showEvent(self, event):
        # 显示时触发重新布局
        super().showEvent(event)
        self._schedule_relayout()
    
    def resizeEvent(self, event):
        # 窗口大小改变时触发重新布局
        super().resizeEvent(event)
        self._schedule_relayout()
