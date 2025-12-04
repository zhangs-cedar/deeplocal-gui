import sys
import os
from PyQt6.QtWidgets import QApplication

# 启用高 DPI 缩放（必须在创建 QApplication 之前设置）
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'

from component import Blocks, Row, Column, Button, Card, Header, ThemeButton, Pages, Label

def on_title_click():
    print("标题被点击了！")

def on_avatar_click():
    print("头像被点击了！")
    
# 工作区页面 - 使用工厂函数延迟加载
def create_workspace_page(pages: Pages):
    with Row() as workspace_page:
        with Card(variant='secondary',margin=5) as card1:
            Label("💼")
            Label("工作区 1")
            Label("这是工作区 1")
        
        with Card(variant='secondary',margin=5) as card2:
            Label("💼")
            Label("工作区 2")
            Label("这是工作区 2")
    return workspace_page

def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        # 先创建 pages 对象并添加到 APP，以便在 Header 中使用
        with Header() as header:
            header.addLeft(Button("🚀", variant='text'))
            header.addLeft(Button("简化示例", variant='text'))
            # 点击按钮切换页面
            header.addCenter(Button("页面1", variant='text'))
            header.addCenter(Button("页面2", variant='text'))
            header.addCenter(Button("页面3", variant='text'))
            header.addRight(ThemeButton(blocks))
            header.addRight(Button("👤", variant='text', on_click=on_avatar_click))
        with Card(variant='secondary',margin=5) as card1:
                    Label("💼")
                    Label("工作区 1")
                    Label("这是工作区 1")
        # 将 pages 添加到 Blocks 中，并配置页面
        pages = Pages()
        blocks.addWidget(pages)
        pages.add_page("页面1", lambda: create_workspace_page(pages))
        pages.add_page("页面2", lambda: create_workspace_page(pages))
        pages.add_page("页面3", lambda: create_workspace_page(pages))
        pages.add_page("页面1-1", lambda: create_workspace_page(pages))
        pages.set_current_page("页面1")
        


    
    blocks.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
