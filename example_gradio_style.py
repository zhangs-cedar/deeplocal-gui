"""
Gradio 风格组件库使用示例
展示如何使用 with 语句构建页面，类似 Gradio API
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from component import (
    GradioBlocks,
    GradioRow,
    GradioColumn,
    GradioButton,
    GradioCard,
    GradioFlow,
    GradioTabs,
    GradioTab,
    GradioThemeToggleButton,
)


def example_basic():
    """示例 1：基本布局，类似 Gradio 的 with 语句"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        with GradioRow():
            # 直接添加按钮，会自动添加到 Row
            btn0 = GradioButton("Button 0")
            btn1 = GradioButton("Button 1")
            btn2 = GradioButton("Button 2")
    
    return demo


def example_scale():
    """示例 2：使用 scale 参数控制相对大小"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        with GradioRow():
            # scale=0: 不扩展，保持最小宽度
            col0 = GradioColumn(scale=0, min_width=150)
            with col0:
                GradioButton("Button 0", variant='primary')
            
            # scale=1: 占据 1 份空间
            col1 = GradioColumn(scale=1, min_width=200)
            with col1:
                GradioButton("Button 1", variant='secondary')
            
            # scale=2: 占据 2 份空间（是 col1 的 2 倍）
            col2 = GradioColumn(scale=2, min_width=200)
            with col2:
                GradioButton("Button 2", variant='stop')
    
    return demo


def example_nested():
    """示例 3：嵌套布局"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        with GradioRow():
            # 左侧列
            with GradioColumn(scale=1):
                GradioButton("Left Top", variant='primary')
                GradioButton("Left Bottom", variant='secondary')
            
            # 右侧列（占据 2 倍空间）
            with GradioColumn(scale=2):
                with GradioRow():
                    GradioButton("Right 1", variant='primary')
                    GradioButton("Right 2", variant='secondary')
                    GradioButton("Right 3", variant='stop')
    
    return demo


def example_flow():
    """示例 4：流式布局（自动换行）"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        with GradioFlow(spacing=12):
            for i in range(10):
                card = GradioCard(
                    header=f"Card {i+1}",
                    shadow='hover',
                )
                card.setMinimumWidth(200)
                card.setMinimumHeight(150)
    
    return demo


def example_tabs():
    """示例 5：标签页"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        tabs = GradioTabs()
        with tabs:
            # Tab 1
            with GradioTab(label="Tab 1"):
                with GradioRow():
                    GradioButton("Button 1", variant='primary')
                    GradioButton("Button 2", variant='secondary')
            
            # Tab 2
            with GradioTab(label="Tab 2"):
                with GradioFlow(spacing=12):
                    for i in range(6):
                        card = GradioCard(header=f"Card {i+1}")
                        card.setMinimumWidth(200)
                        card.setMinimumHeight(120)
    
    return demo


def example_complete():
    """示例 6：完整示例，包含所有功能"""
    demo = GradioBlocks(theme='light')
    
    with demo:
        # 顶部工具栏
        with GradioRow():
            GradioButton("Primary", variant='primary', size='md')
            GradioButton("Secondary", variant='secondary', size='md')
            GradioButton("Stop", variant='stop', size='md')
            GradioThemeToggleButton(blocks=demo, size='md')
        
        # 主要内容区域
        with GradioRow():
            # 左侧边栏
            with GradioColumn(scale=1, min_width=200):
                with GradioFlow(spacing=8):
                    for i in range(5):
                        GradioButton(f"Menu {i+1}", variant='secondary', size='sm')
            
            # 右侧内容区
            with GradioColumn(scale=3):
                tabs = GradioTabs()
                with tabs:
                    with GradioTab(label="布局示例"):
                        with GradioRow():
                            col1 = GradioColumn(scale=1)
                            with col1:
                                GradioCard(header="Column 1", shadow='always')
                            
                            col2 = GradioColumn(scale=2)
                            with col2:
                                GradioCard(header="Column 2", shadow='always')
                    
                    with GradioTab(label="流式布局"):
                        with GradioFlow(spacing=12):
                            for i in range(12):
                                card = GradioCard(
                                    header=f"Card {i+1}",
                                    shadow='hover',
                                )
                                card.setMinimumWidth(200)
                                card.setMinimumHeight(150)
    
    return demo


class ExampleWindow(QMainWindow):
    """示例窗口"""
    
    def __init__(self, example_func, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建示例
        demo = example_func()
        layout.addWidget(demo)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 运行完整示例
    window = ExampleWindow(example_complete, "Gradio 风格组件库 - 完整示例")
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

