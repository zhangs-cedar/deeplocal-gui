from typing import Union, Tuple
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .context import _ContextMixin, _auto_add_to_context, _parse_margin_padding


class Row(QWidget, _ContextMixin):
    def __init__(self, parent=None,
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = 0,
                 spacing: int = 0):
        super().__init__(parent)
        margin_values = _parse_margin_padding(margin)
        padding_values = _parse_margin_padding(padding)
        self._margin = margin_values
        
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(*padding_values)
        self._layout.setSpacing(spacing)
        
        self._apply_style()
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        margin_css = f"margin: {' '.join(map(str, self._margin))}px;"
        self.setStyleSheet(f"QWidget {{ {margin_css} }}")
    
    def addWidget(self, widget: QWidget):
        self._layout.addWidget(widget)
