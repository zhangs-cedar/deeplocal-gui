from typing import List, Union, Tuple
from PyQt6.QtWidgets import QWidget


def _parse_margin_padding(value: Union[int, Tuple[int, ...]]) -> Tuple[int, int, int, int]:
    """解析边距/内边距值，支持 int 或 tuple 格式"""
    if isinstance(value, int):
        return (value, value, value, value)
    elif isinstance(value, tuple):
        if len(value) == 1:
            return (value[0], value[0], value[0], value[0])
        elif len(value) == 2:
            return (value[0], value[1], value[0], value[1])
        elif len(value) == 4:
            return tuple(value)
    return (0, 0, 0, 0)


_context_stack: List[QWidget] = []


def _auto_add_to_context(widget: QWidget):
    # 自动将 widget 添加到当前上下文容器
    if widget.parent() or not _context_stack:
        return
    current = _context_stack[-1]
    if hasattr(current, '_do_relayout'):
        stretch = widget._scale if hasattr(widget, '_scale') else 0
        current.addWidget(widget, stretch)
    elif hasattr(current, 'addWidget'):
        current.addWidget(widget)


class _ContextMixin:
    def __enter__(self):
        # 进入上下文管理器，将自身压入栈
        _context_stack.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出上下文管理器，从栈中弹出自身
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False
