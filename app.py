import sys
from PyQt6.QtWidgets import QApplication
from component import Blocks, Row, Column, Button, Card, Header


def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        header = Header(title="简化示例", icon="🚀", avatar="👤", blocks=blocks)
        blocks.setHeader(header)
        
        with Row():
            Button("按钮 1123124123", variant='secondary')
            Button("按钮 2", variant='secondary')
            Button("按钮 3", variant='secondary')
        
        with Row():
            btn2 = Card(
                title="大按钮 2",
                description="点击大按钮区域会触发 print",
                icon="⭐",   
                variant='secondary'
            )
            Card(
                title="大按钮 1",
                description="点击大按钮区域会触发 print",
                icon="🚀",
                variant='secondary'
            )
            btn3 = Card(
                title="大按钮 3",
                description="点击大按钮区域会触发",
                icon="💡",
                variant='secondary'
            )
            btn2.click(lambda: print("大按钮 2 被点击了！"))
            btn3.click(lambda: print("大按钮 3 被点击了！"))

    
    blocks.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
