"""
Gradio 风格的布局组件
参考 https://www.gradio.app/docs/gradio/row
参考 https://www.gradio.app/docs/gradio/column
参考 https://www.gradio.app/docs/gradio/group
"""
from typing import Optional, Literal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt


class GradioRow(QWidget):
    """
    Gradio 风格的 Row 组件 - 水平布局容器
    参考 Gradio Row: https://www.gradio.app/docs/gradio/row
    所有子元素水平排列
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None,
        scale: Optional[int] = None,
        height: Optional[int] = None,
        max_height: Optional[int] = None,
        min_height: Optional[int] = None,
        equal_height: bool = False,
        show_progress: bool = False
    ):
        """
        初始化 Row 组件
        
        Args:
            parent: 父组件
            variant: 行类型 ('default', 'panel', 'compact')
            visible: 是否可见
            elem_id: HTML DOM id（PyQt6 中作为 objectName）
            elem_classes: HTML DOM class（PyQt6 中用于样式）
            scale: 相对高度（未实现）
            height: 高度（像素）
            max_height: 最大高度（像素）
            min_height: 最小高度（像素）
            equal_height: 是否让所有子元素等高
            show_progress: 是否显示进度动画（未实现）
        """
        super().__init__(parent)
        
        self._variant = variant
        self._equal_height = equal_height
        
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0 if variant == 'compact' else 8)
        
        if elem_id:
            self.setObjectName(elem_id)
        
        if height:
            self.setFixedHeight(height)
        if max_height:
            self.setMaximumHeight(max_height)
        if min_height:
            self.setMinimumHeight(min_height)
        
        self._apply_variant_style()
        self.setVisible(visible)
    
    def _apply_variant_style(self):
        """应用 variant 样式"""
        if self._variant == 'panel':
            self.setStyleSheet("""
                GradioRow {
                    background-color: #F5F5F5;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
        elif self._variant == 'compact':
            self.setStyleSheet("""
                GradioRow {
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("")
    
    def addWidget(self, widget: QWidget, stretch: int = 0):
        """添加子组件"""
        self._layout.addWidget(widget, stretch)
        if self._equal_height:
            widget.setMinimumHeight(self.height() if self.height() > 0 else 100)


class GradioColumn(QWidget):
    """
    Gradio 风格的 Column 组件 - 垂直布局容器
    参考 Gradio Column: https://www.gradio.app/docs/gradio/column
    所有子元素垂直排列，支持 scale 和 min_width
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        scale: int = 1,
        min_width: int = 320,
        variant: Literal['default', 'panel', 'compact'] = 'default',
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None,
        show_progress: bool = False
    ):
        """
        初始化 Column 组件
        
        Args:
            parent: 父组件
            scale: 相对宽度，相比相邻 Column 的宽度比例
            min_width: 最小像素宽度，如果屏幕空间不足会换行
            variant: 列类型 ('default', 'panel', 'compact')
            visible: 是否可见
            elem_id: HTML DOM id（PyQt6 中作为 objectName）
            elem_classes: HTML DOM class（PyQt6 中用于样式）
            show_progress: 是否显示进度动画（未实现）
        """
        super().__init__(parent)
        
        self._scale = scale
        self._min_width = min_width
        self._variant = variant
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0 if variant == 'compact' else 8)
        
        if elem_id:
            self.setObjectName(elem_id)
        
        self.setMinimumWidth(min_width)
        self._apply_variant_style()
        self.setVisible(visible)
    
    def _apply_variant_style(self):
        """应用 variant 样式"""
        if self._variant == 'panel':
            self.setStyleSheet("""
                GradioColumn {
                    background-color: #F5F5F5;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
        elif self._variant == 'compact':
            self.setStyleSheet("""
                GradioColumn {
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("")
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._layout.addWidget(widget)
    
    def get_scale(self) -> int:
        """获取 scale 值"""
        return self._scale
    
    def get_min_width(self) -> int:
        """获取 min_width 值"""
        return self._min_width
    
    def _get_stretch(self) -> int:
        """获取用于布局的拉伸因子"""
        return self._scale


class GradioGroup(QWidget):
    """
    Gradio 风格的 Group 组件 - 分组容器
    参考 Gradio Group: https://www.gradio.app/docs/gradio/group
    将子元素分组，子元素之间没有 padding 或 margin
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[str] = None
    ):
        """
        初始化 Group 组件
        
        Args:
            parent: 父组件
            visible: 是否可见
            elem_id: HTML DOM id（PyQt6 中作为 objectName）
            elem_classes: HTML DOM class（PyQt6 中用于样式）
        """
        super().__init__(parent)
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        if elem_id:
            self.setObjectName(elem_id)
        
        self.setVisible(visible)
    
    def addWidget(self, widget: QWidget):
        """添加子组件"""
        self._layout.addWidget(widget)


if __name__ == "__main__":
    """使用示例"""
    import sys
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout,
        QLabel, QPushButton, QTextEdit, QLineEdit
    )
    from PyQt6.QtCore import Qt
    
    class GradioExampleWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gradio 风格布局组件示例")
            self.setGeometry(100, 100, 1000, 700)
            self.init_ui()
        
        def init_ui(self):
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)
            
            # 示例1: Row - 水平布局
            title1 = QLabel("示例1: Row - 水平布局")
            title1.setStyleSheet("font-size: 16px; font-weight: bold;")
            main_layout.addWidget(title1)
            
            row1 = GradioRow(variant='default')
            row1.addWidget(QLabel("元素1"))
            row1.addWidget(QLabel("元素2"))
            row1.addWidget(QLabel("元素3"))
            main_layout.addWidget(row1)
            
            # 示例2: Row with panel variant
            title2 = QLabel("示例2: Row - panel 样式")
            title2.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
            main_layout.addWidget(title2)
            
            row2 = GradioRow(variant='panel')
            row2.addWidget(QPushButton("按钮1"))
            row2.addWidget(QPushButton("按钮2"))
            row2.addWidget(QPushButton("按钮3"))
            main_layout.addWidget(row2)
            
            # 示例3: Column - 垂直布局
            title3 = QLabel("示例3: Column - 垂直布局")
            title3.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
            main_layout.addWidget(title3)
            
            col1 = GradioColumn(variant='default', min_width=200)
            col1.addWidget(QLabel("文本1"))
            col1.addWidget(QLineEdit("输入框1"))
            col1.addWidget(QPushButton("按钮"))
            main_layout.addWidget(col1)
            
            # 示例4: Column with panel variant
            title4 = QLabel("示例4: Column - panel 样式")
            title4.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
            main_layout.addWidget(title4)
            
            col2 = GradioColumn(variant='panel', min_width=300)
            col2.addWidget(QLabel("标题"))
            col2.addWidget(QTextEdit("内容区域"))
            main_layout.addWidget(col2)
            
            # 示例5: Group - 分组
            title5 = QLabel("示例5: Group - 分组（无间距）")
            title5.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
            main_layout.addWidget(title5)
            
            group = GradioGroup()
            group.addWidget(QLineEdit("First"))
            group.addWidget(QLineEdit("Last"))
            group.addWidget(QPushButton("提交"))
            main_layout.addWidget(group)
            
            # 示例6: Row with Columns (类似 Gradio 的嵌套布局)
            title6 = QLabel("示例6: Row 包含多个 Column（类似 Gradio）")
            title6.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
            main_layout.addWidget(title6)
            
            row_with_cols = GradioRow(variant='default')
            col_a = GradioColumn(scale=1, min_width=150, variant='panel')
            col_a.addWidget(QLabel("Column A (scale=1)"))
            col_a.addWidget(QLineEdit("输入1"))
            col_a.addWidget(QLineEdit("输入2"))
            
            col_b = GradioColumn(scale=2, min_width=200, variant='panel')
            col_b.addWidget(QLabel("Column B (scale=2)"))
            col_b.addWidget(QPushButton("按钮1"))
            col_b.addWidget(QPushButton("按钮2"))
            
            row_with_cols.addWidget(col_a, col_a.get_scale())
            row_with_cols.addWidget(col_b, col_b.get_scale())
            main_layout.addWidget(row_with_cols)
            
            main_layout.addStretch()
    
    def main():
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = GradioExampleWindow()
        window.show()
        sys.exit(app.exec())
    
    main()

