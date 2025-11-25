"""
Element Plus 风格的卡片组件
支持 header、body、footer 三个区域，以及阴影效果
"""
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QEnterEvent, QColor


class Card(QWidget):
    """卡片组件 - 类似于 Element Plus 的 el-card"""
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        shadow: str = 'always',
        body_style: Optional[str] = None,
        header_class: Optional[str] = None,
        body_class: Optional[str] = None,
        footer_class: Optional[str] = None
    ):
        super().__init__(parent)
        
        self._shadow = shadow
        self._body_style = body_style or ""
        self._header_class = header_class or ""
        self._body_class = body_class or ""
        self._footer_class = footer_class or ""
        
        self._header_widget: Optional[QWidget] = None
        self._body_widget: Optional[QWidget] = None
        self._footer_widget: Optional[QWidget] = None
        
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        
        self._shadow_effect: Optional[QGraphicsDropShadowEffect] = None
        self._is_dark_theme = self._detect_dark_theme()
        self._init_ui(header, footer)
        self._update_shadow()
    
    def _init_ui(self, header: Optional[str], footer: Optional[str]):
        """初始化UI"""
        if header:
            self._header_widget = QLabel(header)
            self._header_widget.setObjectName("card_header")
            self._header_widget.setStyleSheet(self._get_header_style())
            self._main_layout.addWidget(self._header_widget)
        
        self._body_widget = QWidget()
        self._body_widget.setObjectName("card_body")
        self._body_layout = QVBoxLayout(self._body_widget)
        self._body_layout.setContentsMargins(20, 20, 20, 20)
        self._body_layout.setSpacing(0)
        
        if self._body_style:
            self._body_widget.setStyleSheet(self._body_style)
        else:
            self._body_widget.setStyleSheet(self._get_body_style())
        
        self._main_layout.addWidget(self._body_widget)
        
        if footer:
            self._footer_widget = QLabel(footer)
            self._footer_widget.setObjectName("card_footer")
            self._footer_widget.setStyleSheet(self._get_footer_style())
            self._main_layout.addWidget(self._footer_widget)
        
        self.setStyleSheet(self._get_card_base_style())
    
    def _detect_dark_theme(self) -> bool:
        """检测当前是否为深色主题"""
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                style_sheet = app.styleSheet().lower()
                if 'dark' in style_sheet or 'black' in style_sheet:
                    return True
            
            widget = self.parent() if self.parent() else self
            for _ in range(10):
                try:
                    palette = widget.palette()
                    bg_color = palette.color(palette.ColorRole.Window)
                    brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
                    if brightness < 128:
                        return True
                    break
                except:
                    pass
                widget = widget.parent() if widget else None
                if not widget:
                    break
        except:
            pass
        return False
    
    def _get_card_base_style(self, hover: bool = False) -> str:
        """获取卡片基础样式"""
        if hover:
            return """
                Card {
                    background-color: #FFFFFF;
                    border: 3px solid #409EFF;
                    border-radius: 4px;
                }
            """
        else:
            return """
                Card {
                    background-color: #FFFFFF;
                    border: 1px solid #EBEEF5;
                    border-radius: 4px;
                }
            """
    
    def _get_header_style(self) -> str:
        """获取 header 样式"""
        return """
            padding: 18px 20px;
            border-bottom: 1px solid #EBEEF5;
            font-size: 16px;
            font-weight: 500;
            color: #303133;
            background-color: #FFFFFF;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        """
    
    def _get_body_style(self) -> str:
        """获取 body 样式"""
        return """
            background-color: #FFFFFF;
            color: #606266;
            font-size: 14px;
        """
    
    def _get_footer_style(self) -> str:
        """获取 footer 样式"""
        return """
            padding: 18px 20px;
            border-top: 1px solid #EBEEF5;
            font-size: 14px;
            color: #909399;
            background-color: #FFFFFF;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
        """
    
    def _update_shadow(self):
        """更新阴影效果"""
        if self._shadow_effect:
            self.setGraphicsEffect(None)
            self._shadow_effect = None
        
        if self._shadow == 'always':
            self._apply_shadow()
        
        self.setStyleSheet(self._get_card_base_style())
    
    def _apply_shadow(self):
        """应用阴影效果"""
        if not self._shadow_effect:
            self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setBlurRadius(12)
            self._shadow_effect.setXOffset(0)
            self._shadow_effect.setYOffset(2)
            
            if self._is_dark_theme:
                self._shadow_effect.setColor(QColor(64, 158, 255, 100))
            else:
                self._shadow_effect.setColor(QColor(0, 0, 0, 50))
        
        try:
            self.setGraphicsEffect(self._shadow_effect)
        except RuntimeError:
            self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setBlurRadius(12)
            self._shadow_effect.setXOffset(0)
            self._shadow_effect.setYOffset(2)
            if self._is_dark_theme:
                self._shadow_effect.setColor(QColor(64, 158, 255, 100))
            else:
                self._shadow_effect.setColor(QColor(0, 0, 0, 50))
            self.setGraphicsEffect(self._shadow_effect)
    
    def _remove_shadow(self):
        """移除阴影效果"""
        try:
            if self._shadow_effect:
                self.setGraphicsEffect(None)
        except RuntimeError:
            self._shadow_effect = None
    
    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件"""
        super().enterEvent(event)
        if self._shadow == 'hover':
            self._apply_shadow()
        self.setStyleSheet(self._get_card_base_style(hover=True))
    
    def leaveEvent(self, event: QEvent):
        """鼠标离开事件"""
        super().leaveEvent(event)
        if self._shadow == 'hover':
            self._remove_shadow()
        self.setStyleSheet(self._get_card_base_style(hover=False))
    
    def setHeaderWidget(self, widget: QWidget):
        """设置自定义 header 组件"""
        if self._header_widget:
            self._main_layout.removeWidget(self._header_widget)
            self._header_widget.setParent(None)
        
        self._header_widget = widget
        if widget:
            widget.setObjectName("card_header")
            widget.setStyleSheet(self._get_header_style())
            self._main_layout.insertWidget(0, widget)
    
    def setFooterWidget(self, widget: QWidget):
        """设置自定义 footer 组件"""
        if self._footer_widget:
            self._main_layout.removeWidget(self._footer_widget)
            self._footer_widget.setParent(None)
        
        self._footer_widget = widget
        if widget:
            widget.setObjectName("card_footer")
            widget.setStyleSheet(self._get_footer_style())
            self._main_layout.addWidget(widget)
    
    def addWidget(self, widget: QWidget):
        """添加内容到 body 区域"""
        self._body_layout.addWidget(widget)
    
    def setBodyStyle(self, style: str):
        """设置 body 样式"""
        self._body_style = style
        if self._body_widget:
            self._body_widget.setStyleSheet(style)
    
    def setShadow(self, shadow: str):
        """设置阴影效果"""
        valid_shadows = ['always', 'hover', 'never']
        if shadow in valid_shadows:
            self._shadow = shadow
            self._update_shadow()
    
    def getHeaderWidget(self) -> Optional[QWidget]:
        """获取 header 组件"""
        return self._header_widget
    
    def getBodyWidget(self) -> QWidget:
        """获取 body 组件"""
        return self._body_widget
    
    def getFooterWidget(self) -> Optional[QWidget]:
        """获取 footer 组件"""
        return self._footer_widget


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel
    )
    from PyQt6.QtCore import Qt
    from app_ui.component.layout import Row, Col
    
    class CardExampleWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Element Plus 风格 Card 组件示例")
            self.setGeometry(100, 100, 1000, 800)
            self.init_ui()
        
        def init_ui(self):
            central_widget = QWidget()
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(central_widget)
            self.setCentralWidget(scroll)
            
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)
            
            row = Row(parent=central_widget, gutter=20)
            main_layout.addWidget(row)
            
            self.add_card_example(row, self.create_basic_card)
            self.add_card_example(row, self.create_simple_card)
            self.add_card_example(row, self.create_image_card)
            self.add_card_example(row, self.create_shadow_always_card)
            self.add_card_example(row, self.create_shadow_hover_card)
            self.add_card_example(row, self.create_shadow_never_card)
        
        def add_card_example(self, row: Row, create_func):
            col = Col(parent=row, span=8, xs=24, sm=12, md=8, lg=8)
            card = create_func()
            col.setWidget(card)
            row.addCol(col)
        
        def create_basic_card(self) -> Card:
            card = Card(header="Card name", footer="Footer content", shadow='always')
            for i in range(1, 5):
                label = QLabel(f"List item {i}")
                label.setStyleSheet("padding: 5px 0; color: #606266;")
                card.addWidget(label)
            return card
        
        def create_simple_card(self) -> Card:
            card = Card(shadow='always')
            for i in range(1, 5):
                label = QLabel(f"List item {i}")
                label.setStyleSheet("padding: 5px 0; color: #606266;")
                card.addWidget(label)
            return card
        
        def create_image_card(self) -> Card:
            card = Card(header="Yummy hamburger", shadow='always')
            image_label = QLabel("🍔\n\nHamburger Image\n(模拟图片)")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("""
                background-color: #F5F7FA;
                padding: 40px;
                border-radius: 4px;
                font-size: 48px;
                color: #909399;
            """)
            image_label.setMinimumHeight(200)
            card.addWidget(image_label)
            return card
        
        def create_shadow_always_card(self) -> Card:
            card = Card(header="Always", shadow='always')
            label = QLabel("此卡片始终显示阴影效果")
            label.setStyleSheet("padding: 20px; color: #606266;")
            card.addWidget(label)
            return card
        
        def create_shadow_hover_card(self) -> Card:
            card = Card(header="Hover", shadow='hover')
            label = QLabel("鼠标悬停时显示阴影效果\n\n将鼠标移到此卡片上试试")
            label.setStyleSheet("padding: 20px; color: #606266;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.addWidget(label)
            return card
        
        def create_shadow_never_card(self) -> Card:
            card = Card(header="Never", shadow='never')
            label = QLabel("此卡片从不显示阴影效果")
            label.setStyleSheet("padding: 20px; color: #606266;")
            card.addWidget(label)
            return card
    
    def main():
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = CardExampleWindow()
        window.show()
        sys.exit(app.exec())
    
    main()
