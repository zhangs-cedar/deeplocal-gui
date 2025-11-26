import sys
from PyQt6.QtWidgets import QApplication
from component.gradio import Blocks, Row, Column, Button, ThemeToggleButton, Card


def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        ThemeToggleButton(blocks)
        
        with Row():
            Button("按钮 1", variant='primary')
            Button("按钮 2", variant='secondary')
            Button("按钮 3", variant='secondary')
        
        with Row():
            btn2 = Card(
                title="大按钮 2",
                description="支持图标、标题和描述文字",
                icon="⭐",
                variant='secondary'
            )
            Card(
                title="大按钮 1",
                description="点击大按钮区域会触发 print",
                icon="🚀",
                variant='primary'
            )
            btn3 = Card(
                title="大按钮 3",
                description="点击大按钮区域会触发",
                icon="💡",
                variant='primary'
            )
            btn2.click(lambda: print("大按钮 2 被点击了！"))
            btn3.click(lambda: print("大按钮 3 被点击了！"))

    
    blocks.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
