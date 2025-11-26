import sys
from PyQt6.QtWidgets import QApplication, QLabel
from component import Blocks, Row, Column, Button, Card, Header, ThemeButton, Pages

def on_title_click():
    print("标题被点击了！")

def on_avatar_click():
    print("头像被点击了！")

def create_project_page():
    with Row() as project_page:
        Card(title="项目 1", description="""这是项目 11111111111111111111111111 \n 1111111111111111111111111111111111111111 \n 1111111111111111111111111111111111111111""", icon="📁", variant='secondary')
        Card(title="项目 2", description="这是项目 2", icon="📁", variant='secondary')
    return project_page

# 模版页面 - 使用工厂函数延迟加载
def create_template_page():
    with Row() as template_page:
        Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
        Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
        Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
        Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
        Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
        Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
        Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
        Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
        Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
        Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
        Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
        Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
        Card(title="模版 1", description="这是模版 1", icon="📄", variant='secondary')
        Card(title="模版 2", description="这是模版 2", icon="📄", variant='secondary')
        Card(title="项目 3", description="这是项目 3", icon="📁", variant='secondary')
    return template_page

# 社区页面 - 使用工厂函数延迟加载
def create_community_page():
    with Row() as community_page:
        Card(title="社区动态", description="查看社区最新动态", icon="👥", variant='secondary')
        Card(title="热门话题", description="浏览热门话题", icon="🔥", variant='secondary')
    return community_page


def main():
    app = QApplication(sys.argv)
    with Blocks(theme='light') as blocks:
        blocks.setWindowTitle("简化示例")
        blocks.resize(800, 600)
        # 创建不同的页面（使用延迟加载，只在点击时才渲染）
        with Pages() as pages:
            # 项目页面 - 使用工厂函数延迟加载
            pages.add_page("项目", create_project_page)
            pages.add_page("模版", create_template_page)
            pages.add_page("社区", create_community_page)
            
        pages.set_current_page("项目") # 默认显示项目页面
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
