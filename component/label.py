from typing import Union, Tuple
from PyQt6.QtWidgets import QLabel
from .context import _ContextMixin, _auto_add_to_context, _parse_margin_padding


class Label(QLabel, _ContextMixin):
    def __init__(self, text: str = "", parent=None,
                 margin: Union[int, Tuple[int, ...]] = 0,
                 padding: Union[int, Tuple[int, ...]] = 0):
        super().__init__(text, parent)
        margin_values = _parse_margin_padding(margin)
        padding_values = _parse_margin_padding(padding)
        self._margin = margin_values
        self._padding = padding_values
        self._apply_style()
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        margin_css = f"margin: {' '.join(map(str, self._margin))}px;"
        padding_css = f"padding: {' '.join(map(str, self._padding))}px;"
        self.setStyleSheet(f"QLabel {{ {margin_css} {padding_css} }}")

