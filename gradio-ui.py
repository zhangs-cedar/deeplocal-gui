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
            # # 1. 顶部工具栏：按钮和主题切换
            # with GradioRow():
            #     GradioButton("Primary", variant='primary', size='md')
            #     GradioButton("Secondary", variant='secondary', size='md')
            #     GradioButton("Stop", variant='stop', size='md')
            #     GradioThemeToggleButton(blocks=demo, size='md')
           
            # 2. 标签页示例
            # 创建 Tabs 并添加到 Blocks（不传 parent，自动添加到上下文）
            tabs = GradioTabs()
            with tabs:
                # Tab 1: 流式布局
                with GradioTab(label="流式布局"):
                    # 创建流式布局并添加到 Tab
                    flow = GradioFlow(spacing=12)
                    # 在流式布局上下文中添加卡片
                    with flow: 
                        for i in range(12):
                            card = GradioCard(
                                header=f"Card {i+1}",
                                shadow='hover',
                            )
                            card.setMinimumWidth(250)
                            card.setMinimumHeight(150)
                            label = QLabel(f"这是卡片 {i+1} 的内容")
                            theme = _get_theme(card)
                            label.setStyleSheet(f"color: {theme.text_secondary};")
                            card.addWidget(label)
                
                # Tab 2: 行布局
                with GradioTab(label="行布局"):
                    with GradioRow():
                        for i in range(3):
                            col = GradioColumn(scale=1, min_width=200)
                            card = GradioCard(
                                header=f"Column {i+1}",
                                shadow='always',
                            )
                            label = QLabel(f"这是列 {i+1} 的内容")
                            theme = _get_theme(card)
                            label.setStyleSheet(f"color: {theme.text_secondary};")
                            card.addWidget(label)
                            col.addWidget(card)
                
                # Tab 3: 卡片示例
                with GradioTab(label="卡片示例"):
                    flow = GradioFlow(spacing=16)
                    with flow:
                        # 基础卡片
                        card1 = GradioCard(
                            header="基础卡片",
                            footer="Footer 内容",
                            shadow='always',
                        )
                        card1.setMinimumWidth(300)
                        for i in range(1, 4):
                            label = QLabel(f"列表项 {i}")
                            theme = _get_theme(card1)
                            label.setStyleSheet(f"padding: 5px 0; color: {theme.text_secondary};")
                            card1.addWidget(label)
                        
                        # 悬停阴影卡片
                        card2 = GradioCard(
                            header="悬停阴影",
                            shadow='hover',
                        )
                        card2.setMinimumWidth(300)
                        label = QLabel("鼠标悬停查看阴影效果")
                        theme = _get_theme(card2)
                        label.setStyleSheet(f"padding: 20px; color: {theme.text_secondary}; text-align: center;")
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        card2.addWidget(label)
                        
                        # 无阴影卡片
                        card3 = GradioCard(
                            header="无阴影",
                            shadow='never',
                        )
                        card3.setMinimumWidth(300)
                        label = QLabel("此卡片没有阴影效果")
                        theme = _get_theme(card3)
                        label.setStyleSheet(f"padding: 20px; color: {theme.text_secondary};")
                        card3.addWidget(label)
                
                # Tab 4: 组合示例
                with GradioTab(label="组合示例"):
                    with GradioGroup():
                        # 第一行：按钮组
                        with GradioRow():
                            GradioButton("操作 1", variant='primary')
                            GradioButton("操作 2", variant='secondary')
                            GradioButton("取消", variant='stop')
                        
                        # 第二行：卡片网格
                        flow = GradioFlow(spacing=12)
                        with flow:
                            for i in range(6):
                                card = GradioCard(
                                    header=f"项目 {i+1}",
                                    shadow='hover',
                                )
                                card.setMinimumWidth(200)
                                card.setMinimumHeight(120)
                                label = QLabel(f"项目 {i+1} 的描述信息")
                                theme = _get_theme(card)
                                label.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
                                card.addWidget(label)
        
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
