"""
Gradio 风格组件库使用示例
按照 Linus 风格：简洁、直接、清晰
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from component import (
    GradioBlocks,
    GradioRow,
    GradioColumn,
    GradioGroup,
    GradioFlow,
    GradioTabs,
    GradioTab,
    GradioButton,
    GradioCard,
    GradioThemeToggleButton,
    _get_theme,
)


class GradioExampleWindow(QMainWindow):
    """Gradio 组件库完整示例"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gradio 风格组件库示例")
        self.setGeometry(100, 100, 1200, 900)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 使用 GradioBlocks 作为主容器
        demo = GradioBlocks(theme='light')
        with demo:
            # 1. 顶部工具栏：按钮和主题切换
            with GradioRow():
                GradioButton("Primary", variant='primary', size='md')
                GradioButton("Secondary", variant='secondary', size='md')
                GradioButton("Stop", variant='stop', size='md')
                GradioThemeToggleButton(blocks=demo, size='md')
           
            # 2. 标签页示例
            # 创建 Tabs 并添加到 Blocks（不传 parent，自动添加到上下文）
    
        
        layout.addWidget(demo)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = GradioExampleWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
