from PyQt6.QtWidgets import QLabel
from .context import _ContextMixin, _auto_add_to_context


class Label(QLabel, _ContextMixin):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        if not parent:
            _auto_add_to_context(self)

