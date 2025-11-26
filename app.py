import sys
from PyQt6.QtWidgets import QApplication, QLabel
from component import Blocks, Row, Column, Button, Card, Header, ThemeButton, Pages

def on_title_click():
    print("标题被点击了！")

def on_avatar_click():
    print("头像被点击了！")


def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        # 创建页面容器
        pages = Pages()
        blocks.addWidget(pages)
        
        # 创建不同的页面
        with pages:
            # 项目页面
            with Column() as project_page:
                with Row():
                    Card(title="项目 1", description="""这是项目 11111111111111111111111111 \n 1111111111111111111111111111111111111111 \n 1111111111111111111111111111111111111111""", icon="📁", variant='secondary')
                    Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 1", description="这是项目 1", icon="📁", variant='secondary')
                    Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 1", description="这是项目 1", icon="📁", variant='secondary')
                    Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 1", description="这是项目 1", icon="📁", variant='secondary')
                    Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
                    Card(title="项目 1", description="这是项目 1", icon="📁", variant='secondary')
                    Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
                    Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
            pages.add_page("项目", project_page)
            
            # 模版页面
            with Column() as template_page:
                with Row():
                    Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
                    Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
            pages.add_page("模版", template_page)
            
            # 社区页面
            with Column() as community_page:
                with Row():
                    Card(title="社区动态", description="查看社区最新动态", icon="👥", variant='secondary')
                    Card(title="热门话题", description="浏览热门话题", icon="🔥", variant='secondary')
            pages.add_page("社区", community_page)
        
        # 使用 with 语法，更优雅
        with Header() as header:
            header.addLeft(Button("🚀", variant='text'))
            header.addLeft(Button("简化示例", variant='text', on_click=on_title_click))
            # 点击按钮切换页面
            header.addCenter(Button("项目", variant='text', on_click=lambda: pages.set_current_page("项目")))
            header.addCenter(Button("模版", variant='text', on_click=lambda: pages.set_current_page("模版")))
            header.addCenter(Button("社区", variant='text', on_click=lambda: pages.set_current_page("社区")))
            header.addRight(ThemeButton(blocks))
            header.addRight(Button("👤", variant='text', on_click=on_avatar_click))
            blocks.setHeader(header)

    
    blocks.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
