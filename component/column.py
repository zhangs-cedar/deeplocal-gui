from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .context import _ContextMixin, _auto_add_to_context


class Column(QWidget, _ContextMixin):
    def __init__(self, parent=None, scale: int = 1, min_width: int = 320):
        # 初始化纵向布局容器
        super().__init__(parent)
        self._scale = scale
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(16)
        self.setMinimumWidth(min_width)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget):
        # 添加 widget 到纵向布局
        self._layout.addWidget(widget)
