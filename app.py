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

def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        # 创建不同的页面（使用延迟加载，只在点击时才渲染）
        with Pages() as pages:
            # 页面页面 - 使用工厂函数延迟加载
            def create_project_page():
                with Row() as project_page:
                    with Card(variant='secondary', on_click=lambda: pages.set_current_page("页面1-1")) as card1:
                        Label("📁")
                        Label("页面 1")
                        Label("这是页面")
                    
                    with Card(variant='secondary') as card2:
                        Label("📁")
                        Label("页面 2")
                        Label("这是页面 2")
                return project_page
            
            # 模版页面 - 使用工厂函数延迟加载
            def create_template_page():
                with Row() as template_page:
                    for i in range(15):
                        with Card(variant='secondary') as card:
                            Label("📄" if i % 3 != 2 else "📁")
                            Label(f"模版 {i+1}" if i % 3 != 2 else f"页面 {i+1}")
                            Label("这是模版" if i % 3 != 2 else "这是页面")
                return template_page
            
            # 社区页面 - 使用工厂函数延迟加载
            def create_community_page():
                with Row() as community_page:
                    with Card(variant='secondary') as card1:
                        Label("👥")
                        Label("页面3")
                        Label("查看社区最新动态")
                    
                    with Card(variant='secondary') as card2:
                        Label("🔥")
                        Label("页面4")
                        Label("浏览热门话题")
                return community_page
            
            # 工作区页面 - 使用工厂函数延迟加载
            def create_workspace_page():
                with Row() as workspace_page:
                    with Card(variant='secondary') as card1:
                        Label("💼")
                        Label("工作区 1")
                        Label("这是工作区 1")
                    
                    with Card(variant='secondary') as card2:
                        Label("💼")
                        Label("工作区 2")
                        Label("这是工作区 2")
                return workspace_page
            
            pages.add_page("页面1", create_project_page)
            pages.add_page("页面2", create_template_page)
            pages.add_page("页面3", create_community_page)
            pages.add_page("页面1-1", create_workspace_page)
            
        pages.set_current_page("页面1") # 默认显示页面页面
        # 使用 with 语法，更优雅
        with Header() as header:
            header.addLeft(Button("🚀", variant='text'))
            header.addLeft(Button("简化示例", variant='text', on_click=on_title_click))
            # 点击按钮切换页面
            header.addCenter(Button("页面1", variant='text', on_click=lambda: pages.set_current_page("页面1")))
            header.addCenter(Button("页面2", variant='text', on_click=lambda: pages.set_current_page("页面2")))
            header.addCenter(Button("页面3", variant='text', on_click=lambda: pages.set_current_page("页面3")))
            header.addRight(ThemeButton(blocks))
            header.addRight(Button("👤", variant='text', on_click=on_avatar_click))
            blocks.setHeader(header)
        
        
    
    blocks.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
