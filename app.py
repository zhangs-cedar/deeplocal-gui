import sys
from PyQt6.QtWidgets import QApplication, QLabel
from component import Blocks, Row, Column, Button, Card, Header


def on_title_click():
    print("标题被点击了！")


def on_avatar_click():
    print("头像被点击了！")


def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
                
        # 使用 with 语法，更优雅
        with Header(blocks=blocks) as header:
            header.addLeft(QLabel("🚀"))  # 左侧添加图标
            title_btn = Button("简化示例", variant='text')
            title_btn.clicked_signal.connect(on_title_click)
            header.addLeft(title_btn)  # 左侧添加标题按钮
            header.addCenter(Button("居中按钮", variant='text'))  # 中间添加按钮
            header.addCenter(Button("居中按钮", variant='text'))  # 中间添加按钮
            header.addCenter(Button("居中按钮", variant='text'))  # 中间添加按钮
            avatar_btn = Button("👤", variant='text')
            avatar_btn.clicked_signal.connect(on_avatar_click)
            header.addRight(avatar_btn)  # 右侧添加头像按钮
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
