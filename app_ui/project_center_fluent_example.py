"""
使用 qfluentwidgets 简化后的代码示例
安装: pip install qfluentwidgets
"""

from qfluentwidgets import (
    CardWidget, BodyLabel, CaptionLabel, 
    PrimaryPushButton, PushButton,
    ScrollArea, VBoxLayout, HBoxLayout,
    FluentIcon, IconWidget
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta

from models import Project
from utils import format_datetime


class ProjectCard(CardWidget):
    """项目卡片 - 使用 qfluentwidgets 简化"""
    
    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self.setFixedSize(280, 140)
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI - 代码大幅简化"""
        # 项目名称
        name_label = BodyLabel(self.project.name, self)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # 项目描述
        desc_label = CaptionLabel(self.project.desc or "无描述", self)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(40)
        
        # 时间标签
        time_str = self._format_time(self.project.created_at)
        time_label = CaptionLabel(time_str, self)
        
        # 添加到布局（自动布局，无需手动设置margins）
        self.vBoxLayout.addWidget(name_label)
        self.vBoxLayout.addWidget(desc_label)
        self.vBoxLayout.addWidget(time_label)
        self.vBoxLayout.addStretch(1)
    
    def _format_time(self, dt: datetime):
        now = datetime.now()
        diff = now - dt
        if diff < timedelta(hours=1):
            return f"{int(diff.total_seconds() / 60)}分钟前"
        elif diff < timedelta(days=1):
            return f"{int(diff.total_seconds() / 3600)}小时前"
        elif diff < timedelta(days=7):
            return f"{diff.days}天前"
        else:
            return format_datetime(dt)


class ProjectListWidgetFluent(QWidget):
    """使用 qfluentwidgets 的项目列表 - 代码简化版"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent.main_window if parent else None
        self.selected_card = None
        self.project_cards = []
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题（使用 BodyLabel 自动样式）
        title = BodyLabel("项目中心", self)
        layout.addWidget(title)
        
        # 搜索框（qfluentwidgets 有 LineEdit 组件，这里简化示例）
        # search = LineEdit(self)
        # search.setPlaceholderText("搜索项目...")
        # layout.addWidget(search)
        
        # 滚动区域（自动处理滚动）
        scroll = ScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # 新建按钮（自动样式，无需设置 objectName）
        btn_new = PrimaryPushButton("+ 新建项目", self)
        btn_new.clicked.connect(self.create_project)
        layout.addWidget(btn_new)
    
    def load_projects(self, projects: list):
        """加载项目 - 代码更简洁"""
        for card in self.project_cards:
            card.setParent(None)
        self.project_cards.clear()
        self.selected_card = None
        
        for project in projects:
            # 创建卡片（一行代码，自动样式）
            card = ProjectCard(project, self)
            card.clicked.connect(lambda checked, p=project: self._on_card_clicked(card, p))
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, card)
            self.project_cards.append(card)
    
    def _on_card_clicked(self, card, project):
        """卡片点击处理 - 使用组件库的选中状态"""
        if self.selected_card:
            self.selected_card.setSelected(False)  # 组件库提供的方法
        
        card.setSelected(True)  # 自动处理样式
        self.selected_card = card
        self.selected_project = project
        
        if self.main_window:
            self.main_window.show_project_detail(project)
    
    def create_project(self):
        # 创建项目逻辑...
        pass


# 对比：原代码 vs 组件库代码
"""
原代码创建卡片需要：
- 创建 QFrame
- 设置 ObjectName
- 设置 Cursor
- 创建 Layout
- 设置 ContentsMargins
- 创建多个 Label
- 设置每个 Label 的 ObjectName
- 手动绑定事件处理
- 手动管理样式

使用 qfluentwidgets 后：
- 继承 CardWidget（自动样式）
- 使用 BodyLabel/CaptionLabel（自动样式）
- 自动布局管理
- 内置点击事件
- 内置选中状态管理

代码量减少约 60-70%！
"""

