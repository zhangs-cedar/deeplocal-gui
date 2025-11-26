from typing import Optional, Literal, List, Union
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QGridLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QEvent
from PyQt6.QtGui import QIcon, QEnterEvent

_context_stack: List[QWidget] = []


class Theme:
    def __init__(self, mode: Literal['light', 'dark'] = 'light'):
        self.mode = mode
        if mode == 'light':
            self.bg = "#FFFFFF"
            self.bg_secondary = "#F5F5F7"
            self.text = "#000000"
            self.text_secondary = "#6E6E73"
            self.primary = "#007AFF"
            self.primary_hover = "#0051D5"
            self.border = "#D1D1D6"
        else:
            self.bg = "#1C1C1E"
            self.bg_secondary = "#2C2C2E"
            self.text = "#FFFFFF"
            self.text_secondary = "#98989D"
            self.primary = "#0A84FF"
            self.primary_hover = "#409CFF"
            self.border = "#38383A"


def _get_theme(widget: QWidget) -> Theme:
    current = widget
    while current:
        if isinstance(current, Blocks):
            return current._theme
        current = current.parent()
    return Theme('light')


def _auto_add_to_context(widget: QWidget):
    if widget.parent() or not _context_stack:
        return
    current = _context_stack[-1]
    if isinstance(current, Row):
        stretch = widget._scale if isinstance(widget, Column) else 0
        current.addWidget(widget, stretch)
    elif isinstance(current, (Column, Blocks)):
        current.addWidget(widget)


class _ContextMixin:
    def __enter__(self):
        _context_stack.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False


class Blocks(QWidget, _ContextMixin):
    def __init__(self, parent=None, theme: Union[str, Theme] = 'light'):
        super().__init__(parent)
        self._theme = Theme(theme) if isinstance(theme, str) else (theme or Theme('light'))
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content = QWidget()
        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(20)
        self._layout.addStretch()
        
        scroll.setWidget(content)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        self._apply_theme()
    
    def _apply_theme(self):
        bg = self._theme.bg
        self.setStyleSheet(f"QWidget {{ background-color: {bg}; }}")
        for child in self.findChildren(QWidget):
            if isinstance(child, (Row, Column, Button, Card, ThemeToggleButton)):
                if hasattr(child, '_apply_style'):
                    child._apply_style()
    
    def toggle_theme(self):
        self._theme = Theme('dark' if self._theme.mode == 'light' else 'light')
        self._apply_theme()
    
    def addWidget(self, widget: QWidget):
        self._layout.removeItem(self._layout.itemAt(self._layout.count() - 1))
        self._layout.addWidget(widget)
        self._layout.addStretch()


class Row(QWidget, _ContextMixin):
    def __init__(self, parent=None):
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
        self._widgets.append(widget)
        self._schedule_relayout()
    
    def _schedule_relayout(self):
        self._relayout_timer.start(10)
    
    def _do_relayout(self):
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
        
        min_w = 120
        cols = max(1, (available + spacing) // (min_w + spacing))
        
        for i, widget in enumerate(self._widgets):
            if widget.parent() != self:
                widget.setParent(self)
            self._layout.addWidget(widget, i // cols, i % cols)
    
    def showEvent(self, event):
        super().showEvent(event)
        self._schedule_relayout()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._schedule_relayout()


class Column(QWidget, _ContextMixin):
    def __init__(self, parent=None, scale: int = 1, min_width: int = 320):
        super().__init__(parent)
        self._scale = scale
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(16)
        self.setMinimumWidth(min_width)
        if not parent:
            _auto_add_to_context(self)
    
    def addWidget(self, widget: QWidget):
        self._layout.addWidget(widget)


class Button(QPushButton):
    clicked_signal = pyqtSignal()
    
    def __init__(self, value: str = "Run", variant: Literal['primary', 'secondary'] = 'secondary', parent=None):
        super().__init__(str(value), parent)
        self._variant = variant
        self.clicked.connect(self._on_clicked)
        self._apply_style()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        theme = _get_theme(self)
        if self._variant == 'primary':
            bg, hover, color = theme.primary, theme.primary_hover, "#FFFFFF"
        else:
            bg, hover, color = theme.bg_secondary, theme.border, theme.text
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: 1px solid {theme.border};
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
        """)
    
    def _on_clicked(self):
        self.clicked_signal.emit()
    
    def click(self, fn=None):
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal


class Card(QFrame, _ContextMixin):
    clicked_signal = pyqtSignal()
    
    def __init__(self, title: str = "", description: str = "", icon: Union[str, Path] = None, 
                 variant: Literal['primary', 'secondary'] = 'secondary', parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self._title = title
        self._description = description
        self._icon = icon
        self._variant = variant
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        if icon:
            icon_label = QLabel()
            try:
                icon_path = Path(icon) if isinstance(icon, str) else icon
                if icon_path.exists():
                    icon_label.setPixmap(QIcon(str(icon_path)).pixmap(32, 32))
                else:
                    icon_label.setText(str(icon))
                    icon_label.setStyleSheet("font-size: 24px;")
            except:
                icon_label.setText(str(icon))
                icon_label.setStyleSheet("font-size: 24px;")
            layout.addWidget(icon_label)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 16px; font-weight: 600;")
            layout.addWidget(title_label)
        
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("font-size: 13px; opacity: 0.7;")
            layout.addWidget(desc_label)
        
        layout.addStretch()
        
        self.setObjectName("Card")
        self._apply_style()
        if not parent:
            _auto_add_to_context(self)
    
    def _apply_style(self):
        theme = _get_theme(self)
        if self._variant == 'primary':
            bg, hover, color = theme.primary, theme.primary_hover, "#FFFFFF"
        else:
            bg, hover, color = theme.bg_secondary, theme.border, theme.text
        
        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {bg};
                border: 1px solid {theme.border};
                border-radius: 12px;
            }}
            QFrame#Card:hover {{
                background-color: {hover};
                border-color: {theme.border};
            }}
            QFrame#Card > QLabel {{
                color: {color};
                background-color: transparent;
            }}
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())
            if child and isinstance(child, (QPushButton, Button)):
                return
            self.clicked_signal.emit()
        super().mousePressEvent(event)
    
    def click(self, fn=None):
        if fn:
            return self.clicked_signal.connect(fn)
        return self.clicked_signal
    
    def addWidget(self, widget: QWidget):
        layout = self.layout()
        layout.insertWidget(layout.count() - 1, widget)


class ThemeToggleButton(Button):
    def __init__(self, blocks: Blocks = None, parent=None):
        super().__init__("", 'secondary', parent)
        if blocks:
            self._blocks = blocks
        else:
            current = self.parent()
            while current:
                if isinstance(current, Blocks):
                    self._blocks = current
                    break
                current = current.parent()
            else:
                raise ValueError("需要 Blocks 实例")
        
        self.clicked_signal.connect(self._toggle)
        self._update_text()
    
    def _update_text(self):
        if self._blocks._theme.mode == 'light':
            self.setText("🌙")
        else:
            self.setText("☀️")
    
    def _toggle(self):
        self._blocks.toggle_theme()
        self._update_text()
