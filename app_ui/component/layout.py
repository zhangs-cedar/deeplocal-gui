"""
Element Plus 风格的流式布局组件
基于 24 分栏的栅格系统，支持响应式布局
"""
from typing import Optional, Union, Dict, List
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QRect, QPoint
from PyQt6.QtGui import QResizeEvent


class Row(QWidget):
    """
    行组件 - 类似于 Element Plus 的 el-row
    支持 gutter（列间距）、justify（水平对齐）、align（垂直对齐）
    """
    
    # 响应式断点（像素宽度）
    BREAKPOINTS = {
        'xs': 0,      # < 768px
        'sm': 768,    # >= 768px
        'md': 992,    # >= 992px
        'lg': 1200,   # >= 1200px
        'xl': 1920    # >= 1920px
    }
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        gutter: int = 0,
        justify: str = 'start',
        align: Optional[str] = None,
        tag: str = 'div'
    ):
        """
        初始化 Row 组件
        
        Args:
            parent: 父组件
            gutter: 列间距（像素）
            justify: 水平对齐方式 ('start', 'end', 'center', 'space-between', 'space-around', 'space-evenly')
            align: 垂直对齐方式 ('top', 'middle', 'bottom')
            tag: 自定义元素标签（PyQt6 中不使用，保留以兼容 API）
        """
        super().__init__(parent)
        self.gutter = gutter
        self.justify = justify
        self.align = align or 'top'
        self._cols: List[Col] = []
        self._current_breakpoint = 'xs'
        self._rows: List[List[Col]] = []  # 存储每行的列
        
        # 设置最小尺寸
        self.setMinimumSize(100, 50)
        
    def addWidget(self, widget: QWidget):
        """添加子组件（自动识别 Col 组件）"""
        if isinstance(widget, Col):
            self._cols.append(widget)
            widget.setParent(self)
        else:
            # 如果不是 Col，自动包装
            col = Col(parent=self, span=24)
            col.setWidget(widget)
            self._cols.append(col)
        self._update_layout()
    
    def addCol(self, col: 'Col'):
        """添加 Col 组件"""
        self._cols.append(col)
        col.setParent(self)
        self._update_layout()
    
    def _get_current_breakpoint(self) -> str:
        """根据当前宽度获取响应式断点"""
        width = self.width()
        if width >= self.BREAKPOINTS['xl']:
            return 'xl'
        elif width >= self.BREAKPOINTS['lg']:
            return 'lg'
        elif width >= self.BREAKPOINTS['md']:
            return 'md'
        elif width >= self.BREAKPOINTS['sm']:
            return 'sm'
        else:
            return 'xs'
    
    def _update_layout(self):
        """更新布局"""
        if not self._cols:
            return
        
        self._current_breakpoint = self._get_current_breakpoint()
        self._layout_cols()
        self.update()
    
    def _layout_cols(self):
        """布局 Col 组件 - 支持自动换行"""
        if not self._cols:
            return
        
        # 计算可用宽度
        available_width = self.width()
        if available_width <= 0:
            available_width = self.sizeHint().width() or 800
        
        # 将列分组到行中（每行最多 24 列）
        self._rows = []
        current_row: List[Dict] = []
        current_row_span = 0
        
        for col in self._cols:
            span = col.get_span(self._current_breakpoint)
            offset = col.get_offset(self._current_breakpoint)
            total_span = span + offset
            
            # 检查是否需要换行
            if current_row_span + total_span > 24 and current_row:
                self._rows.append(current_row)
                current_row = []
                current_row_span = 0
            
            current_row.append({
                'col': col,
                'span': span,
                'offset': offset
            })
            current_row_span += total_span
        
        if current_row:
            self._rows.append(current_row)
        
        # 计算每列的实际宽度
        base_width = available_width / 24
        
        # 布局每一行
        current_y = 0
        total_height = 0
        
        for row_configs in self._rows:
            row_height = 0
            current_x = 0
            
            # 计算这一行的总 span（包括 offset）
            row_total_span = sum(c['span'] + c['offset'] for c in row_configs)
            row_total_width = row_total_span * base_width
            row_gutter_width = (len(row_configs) - 1) * self.gutter
            row_actual_width = row_total_width + row_gutter_width
            
            # 根据 justify 计算起始位置和间距
            row_gutter = self.gutter  # 保存原始 gutter 值
            if self.justify == 'end':
                current_x = available_width - row_actual_width
            elif self.justify == 'center':
                current_x = (available_width - row_actual_width) / 2
            elif self.justify == 'space-between' and len(row_configs) > 1:
                # space-between: 首尾对齐，中间平均分布
                used_width = sum(c['span'] * base_width for c in row_configs)
                remaining_width = available_width - used_width
                row_gutter = remaining_width / (len(row_configs) - 1) if len(row_configs) > 1 else 0
            elif self.justify == 'space-around' and len(row_configs) > 1:
                # space-around: 每个元素周围空间相等
                used_width = sum(c['span'] * base_width for c in row_configs)
                remaining_width = available_width - used_width
                gutter_around = remaining_width / len(row_configs) / 2
                row_gutter = gutter_around * 2
                current_x = gutter_around
            elif self.justify == 'space-evenly' and len(row_configs) > 1:
                # space-evenly: 元素之间和两端空间都相等
                used_width = sum(c['span'] * base_width for c in row_configs)
                remaining_width = available_width - used_width
                row_gutter = remaining_width / (len(row_configs) + 1)
                current_x = row_gutter
            
            # 布局这一行的每一列
            for i, config in enumerate(row_configs):
                col = config['col']
                span = config['span']
                offset = config['offset']
                
                # 计算位置和大小
                col_width = base_width * span
                col_x = current_x + base_width * offset
                
                # 获取列的高度
                col_height = self._get_col_height(col)
                row_height = max(row_height, col_height)
                
                # 根据 align 调整垂直位置
                y_offset = 0
                if self.align == 'middle':
                    y_offset = (row_height - col_height) / 2
                elif self.align == 'bottom':
                    y_offset = row_height - col_height
                
                # 设置 Col 的位置和大小
                col.setGeometry(
                    int(col_x),
                    int(current_y + y_offset),
                    int(col_width),
                    int(col_height)
                )
                col.show()
                
                # 更新位置
                current_x = col_x + col_width + row_gutter
            
            current_y += row_height + self.gutter
            total_height += row_height
        
        # 设置行高度
        if total_height > 0:
            self.setMinimumHeight(int(total_height))
    
    def _get_col_height(self, col: 'Col') -> int:
        """获取 Col 的高度"""
        widget = col.get_widget()
        if widget:
            hint = widget.sizeHint()
            if hint.height() > 0:
                return hint.height()
            # 尝试获取实际高度
            widget_height = widget.height()
            if widget_height > 0:
                return widget_height
        # 默认高度
        return col.height() if col.height() > 0 else 50
    
    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时重新布局"""
        super().resizeEvent(event)
        old_breakpoint = self._current_breakpoint
        self._current_breakpoint = self._get_current_breakpoint()
        
        # 如果断点改变或尺寸改变，需要重新布局
        if old_breakpoint != self._current_breakpoint or event.oldSize() != event.size():
            self._update_layout()
    
    def setGutter(self, gutter: int):
        """设置列间距"""
        self.gutter = gutter
        self._update_layout()
    
    def setJustify(self, justify: str):
        """设置水平对齐方式"""
        valid_justify = ['start', 'end', 'center', 'space-between', 'space-around', 'space-evenly']
        if justify in valid_justify:
            self.justify = justify
            self._update_layout()
    
    def setAlign(self, align: str):
        """设置垂直对齐方式"""
        valid_align = ['top', 'middle', 'bottom']
        if align in valid_align:
            self.align = align
            self._update_layout()


class Col(QWidget):
    """
    列组件 - 类似于 Element Plus 的 el-col
    支持 span（占据列数）、offset（左侧间隔）、响应式布局
    """
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        span: int = 24,
        offset: int = 0,
        push: int = 0,
        pull: int = 0,
        xs: Optional[Union[int, Dict]] = None,
        sm: Optional[Union[int, Dict]] = None,
        md: Optional[Union[int, Dict]] = None,
        lg: Optional[Union[int, Dict]] = None,
        xl: Optional[Union[int, Dict]] = None,
        tag: str = 'div'
    ):
        """
        初始化 Col 组件
        
        Args:
            parent: 父组件（通常是 Row）
            span: 栅格占据的列数（1-24）
            offset: 栅格左侧的间隔格数
            push: 栅格向右移动格数
            pull: 栅格向左移动格数
            xs: <768px 响应式栅格数或属性对象
            sm: >=768px 响应式栅格数或属性对象
            md: >=992px 响应式栅格数或属性对象
            lg: >=1200px 响应式栅格数或属性对象
            xl: >=1920px 响应式栅格数或属性对象
            tag: 自定义元素标签（PyQt6 中不使用，保留以兼容 API）
        """
        super().__init__(parent)
        self._span = span
        self._offset = offset
        self._push = push
        self._pull = pull
        
        # 响应式配置
        self._responsive = {
            'xs': self._parse_responsive(xs),
            'sm': self._parse_responsive(sm),
            'md': self._parse_responsive(md),
            'lg': self._parse_responsive(lg),
            'xl': self._parse_responsive(xl)
        }
        
        self._widget: Optional[QWidget] = None
        
    def _parse_responsive(self, value: Optional[Union[int, Dict]]) -> Optional[Dict]:
        """解析响应式配置"""
        if value is None:
            return None
        if isinstance(value, int):
            return {'span': value}
        if isinstance(value, dict):
            return value
        return None
    
    def get_span(self, breakpoint: str) -> int:
        """获取指定断点的 span 值"""
        resp = self._responsive.get(breakpoint)
        if resp and 'span' in resp:
            return resp['span']
        return self._span
    
    def get_offset(self, breakpoint: str) -> int:
        """获取指定断点的 offset 值"""
        resp = self._responsive.get(breakpoint)
        if resp and 'offset' in resp:
            return resp['offset']
        return self._offset
    
    def setWidget(self, widget: QWidget):
        """设置内部组件"""
        if self._widget:
            self._widget.setParent(None)
        self._widget = widget
        if widget:
            widget.setParent(self)
            widget.setGeometry(0, 0, self.width(), self.height())
    
    def get_widget(self) -> Optional[QWidget]:
        """获取内部组件"""
        return self._widget
    
    def resizeEvent(self, event: QResizeEvent):
        """调整大小时更新内部组件"""
        super().resizeEvent(event)
        if self._widget:
            self._widget.setGeometry(0, 0, self.width(), self.height())
    
    def setSpan(self, span: int):
        """设置占据的列数"""
        self._span = max(1, min(24, span))
        if isinstance(self.parent(), Row):
            self.parent()._update_layout()
    
    def setOffset(self, offset: int):
        """设置左侧间隔"""
        self._offset = max(0, offset)
        if isinstance(self.parent(), Row):
            self.parent()._update_layout()
    
    def setResponsive(self, breakpoint: str, config: Union[int, Dict]):
        """设置响应式配置"""
        if breakpoint in self._responsive:
            self._responsive[breakpoint] = self._parse_responsive(config)
            if isinstance(self.parent(), Row):
                self.parent()._update_layout()

if __name__ == "__main__":
    """
    使用示例：演示 Row 和 Col 组件的各种用法
    """
    import sys
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QLabel, QPushButton, QLineEdit, QTextEdit
    )
    from PyQt6.QtCore import Qt
    
    class LayoutExampleWindow(QMainWindow):
        """布局组件示例窗口"""
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Element Plus 风格布局组件示例")
            self.setGeometry(100, 100, 1200, 800)
            self.init_ui()
        
        def init_ui(self):
            """初始化UI"""
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)
            
   
            # 示例6: 响应式布局
            self.add_example_section(main_layout, "示例6: 响应式布局（调整窗口大小查看效果）", self.create_responsive_layout)
        
        def add_example_section(self, parent_layout, title, create_func):
            """添加示例区域"""
            # 标题
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #409EFF; margin: 10px 0;")
            parent_layout.addWidget(title_label)
            
            # 示例内容
            example_widget = create_func()
            parent_layout.addWidget(example_widget)
        
        def create_basic_layout(self) -> QWidget:
            """创建基础布局示例"""
            row = Row(gutter=10)
            
            # 24列（全宽）
            col1 = Col(parent=row, span=24)
            label1 = QLabel("24列（全宽）")
            label1.setStyleSheet("background: #409EFF; color: white; padding: 10px; border-radius: 4px;")
            label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setWidget(label1)
            row.addCol(col1)
            
            # 12列 + 12列
            col2 = Col(parent=row, span=12)
            label2 = QLabel("12列")
            label2.setStyleSheet("background: #67C23A; color: white; padding: 10px; border-radius: 4px;")
            label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col2.setWidget(label2)
            row.addCol(col2)
            
            col3 = Col(parent=row, span=12)
            label3 = QLabel("12列")
            label3.setStyleSheet("background: #E6A23C; color: white; padding: 10px; border-radius: 4px;")
            label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col3.setWidget(label3)
            row.addCol(col3)
            
            # 8列 + 8列 + 8列
            for i, color in enumerate(["#F56C6C", "#909399", "#409EFF"], 1):
                col = Col(parent=row, span=8)
                label = QLabel(f"8列-{i}")
                label.setStyleSheet(f"background: {color}; color: white; padding: 10px; border-radius: 4px;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col.setWidget(label)
                row.addCol(col)
            
            return row
        
        def create_gutter_layout(self) -> QWidget:
            """创建带间距的布局示例"""
            row = Row(gutter=20)
            
            for i, span in enumerate([6, 6, 6, 6], 1):
                col = Col(parent=row, span=span)
                label = QLabel(f"{span}列")
                label.setStyleSheet("background: #67C23A; color: white; padding: 10px; border-radius: 4px;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col.setWidget(label)
                row.addCol(col)
            
            return row
        
        def create_mixed_layout(self) -> QWidget:
            """创建混合布局示例"""
            row = Row(gutter=10)
            
            # 16列 + 8列
            col1 = Col(parent=row, span=16)
            label1 = QLabel("16列（主内容区）")
            label1.setStyleSheet("background: #409EFF; color: white; padding: 20px; border-radius: 4px;")
            label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setWidget(label1)
            row.addCol(col1)
            
            col2 = Col(parent=row, span=8)
            label2 = QLabel("8列（侧边栏）")
            label2.setStyleSheet("background: #E6A23C; color: white; padding: 20px; border-radius: 4px;")
            label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col2.setWidget(label2)
            row.addCol(col2)
            
            return row
        
        def create_offset_layout(self) -> QWidget:
            """创建列偏移示例"""
            row = Row(gutter=10)
            
            # 无偏移
            col1 = Col(parent=row, span=6, offset=0)
            label1 = QLabel("6列，无偏移")
            label1.setStyleSheet("background: #409EFF; color: white; padding: 10px; border-radius: 4px;")
            label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setWidget(label1)
            row.addCol(col1)
            
            # 偏移6列
            col2 = Col(parent=row, span=6, offset=6)
            label2 = QLabel("6列，偏移6列")
            label2.setStyleSheet("background: #67C23A; color: white; padding: 10px; border-radius: 4px;")
            label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col2.setWidget(label2)
            row.addCol(col2)
            
            # 偏移6列
            col3 = Col(parent=row, span=6, offset=6)
            label3 = QLabel("6列，偏移6列")
            label3.setStyleSheet("background: #E6A23C; color: white; padding: 10px; border-radius: 4px;")
            label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col3.setWidget(label3)
            row.addCol(col3)
            
            return row
        
        def create_justify_layout(self) -> QWidget:
            """创建对齐方式示例"""
            row = Row(gutter=10, justify='center')
            
            for i, span in enumerate([4, 4, 4], 1):
                col = Col(parent=row, span=span)
                label = QLabel(f"{span}列")
                label.setStyleSheet("background: #909399; color: white; padding: 10px; border-radius: 4px;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col.setWidget(label)
                row.addCol(col)
            
            return row
        
        def create_responsive_layout(self) -> QWidget:
            """创建响应式布局示例"""
            row = Row(gutter=10)
            
            # 响应式配置：xs=24, sm=12, md=8, lg=6, xl=4
            for i in range(6):
                col = Col(
                    parent=row, 
                    span=4,
                    xs=24,  # 小屏幕：全宽
                    sm=12,  # 中等屏幕：一半
                    md=8,   # 大屏幕：1/3
                    lg=6,   # 更大屏幕：1/4
                    xl=4    # 超大屏幕：1/6
                )
                label = QLabel(f"响应式列 {i+1}\n调整窗口大小查看效果")
                label.setStyleSheet("background: #F56C6C; color: white; padding: 15px; border-radius: 4px;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col.setWidget(label)
                row.addCol(col)
            
            return row
    
    def main():
        """主函数"""
        app = QApplication(sys.argv)
        
        # 设置应用样式
        app.setStyle('Fusion')
        
        window = LayoutExampleWindow()
        window.show()
        
        sys.exit(app.exec())
    
    main()
