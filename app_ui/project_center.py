from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import (
    CardWidget, SimpleCardWidget, BodyLabel, CaptionLabel, 
    PrimaryPushButton, PushButton, LineEdit,
    ScrollArea, VBoxLayout
)
from datetime import datetime, timedelta

from models import Project
from utils import format_datetime
from cedar.utils import print


class ProjectCard(SimpleCardWidget):
    """项目卡片组件 - 使用 qfluentwidgets 简化"""
    
    project_clicked = pyqtSignal(object)  # 项目点击信号，传递 project 对象
    
    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self.setFixedSize(280, 120)
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = VBoxLayout(self)
        
        # 项目名称
        name_label = BodyLabel(self.project.name, self)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(name_label)
        
        # 项目描述
        desc = self.project.desc or "无描述"
        desc_label = CaptionLabel(desc, self)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(40)
        layout.addWidget(desc_label)
        
        # 时间标签
        time_str = self._format_time(self.project.created_at)
        time_label = CaptionLabel(time_str, self)
        layout.addWidget(time_label)
        
        layout.addStretch(1)
    
    def _format_time(self, dt: datetime) -> str:
        """格式化时间显示"""
        now = datetime.now()
        diff = now - dt
        
        if diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes}分钟前"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}小时前"
        elif diff < timedelta(days=7):
            return f"{diff.days}天前"
        else:
            return format_datetime(dt)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件 - 重写以发射自定义信号"""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.project_clicked.emit(self.project)


class ProjectListWidget(QWidget):
    """项目列表侧边栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent.main_window if parent else None
        self.selected_project = None
        self.selected_card = None
        self.project_cards = []
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 标题
        title = BodyLabel("项目中心", self)
        layout.addWidget(title)
        
        # 搜索框
        self.search_box = LineEdit(self)
        self.search_box.setPlaceholderText("搜索项目...")
        layout.addWidget(self.search_box)
        
        # 滚动区域
        scroll = ScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # 新建项目按钮
        btn_new = PrimaryPushButton("新建项目", self)
        btn_new.clicked.connect(self.create_project)
        layout.addWidget(btn_new)
    
    def load_projects(self, projects: list):
        """加载项目列表"""
        # 清除现有卡片
        for card in self.project_cards:
            card.setParent(None)
        self.project_cards.clear()
        self.selected_card = None
        self.selected_project = None
        
        # 创建新卡片
        for project in projects:
            card = ProjectCard(project, self)
            card.project_clicked.connect(self._on_card_clicked)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, card)
            self.project_cards.append(card)
    
    def _on_card_clicked(self, project: Project):
        """卡片点击处理"""
        # 找到对应的卡片
        card = None
        for c in self.project_cards:
            if c.project.id == project.id:
                card = c
                break
        
        if not card or self.selected_card == card:
            return
        
        # 更新选中状态 - Linux 风格，使用简单的边框
        if self.selected_card:
            self.selected_card.setStyleSheet("")  # 恢复默认样式
        
        card.setStyleSheet("border: 2px solid #0078d4;")  # 选中边框
        
        self.selected_card = card
        self.selected_project = project
        
        # 显示项目详情
        if self.main_window:
            self.main_window.show_project_detail(project)
    
    def create_project(self):
        """创建新项目"""
        name, ok = QInputDialog.getText(self, "新建项目", "项目名称:")
        if not ok or not name.strip():
            print("[操作] 取消创建项目")
            return
        
        desc, ok = QInputDialog.getText(self, "新建项目", "项目描述:")
        if not ok:
            desc = ""
        
        try:
            if self.main_window:
                project = self.main_window.create_project(name.strip(), desc.strip())
                if project:
                    self.load_projects(self.main_window.get_projects())
                    QMessageBox.information(self, "成功", f"项目 '{name}' 创建成功")
        except Exception as e:
            print(f"[错误] 创建项目失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"创建项目失败: {str(e)}")


class ProjectDetailWidget(QWidget):
    """项目详情面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent.main_window if parent and hasattr(parent, 'main_window') else None
        self.current_project = None
        self.selected_workspace = None
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 项目详情卡片
        self.detail_card = CardWidget(self)
        detail_layout = VBoxLayout(self.detail_card)
        
        title = BodyLabel("项目详情", self.detail_card)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        detail_layout.addWidget(title)
        
        self.name_label = BodyLabel("", self.detail_card)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        detail_layout.addWidget(self.name_label)
        
        self.desc_label = CaptionLabel("", self.detail_card)
        self.desc_label.setWordWrap(True)
        detail_layout.addWidget(self.desc_label)
        
        self.time_label = CaptionLabel("", self.detail_card)
        detail_layout.addWidget(self.time_label)
        
        self.path_label = CaptionLabel("", self.detail_card)
        detail_layout.addWidget(self.path_label)
        
        layout.addWidget(self.detail_card)
        
        # 工作区卡片
        workspace_card = CardWidget(self)
        ws_layout = VBoxLayout(workspace_card)
        
        ws_title = BodyLabel("工作区", workspace_card)
        ws_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        ws_layout.addWidget(ws_title)
        
        self.workspace_grid = QWidget(workspace_card)
        self.grid_layout = QGridLayout(self.workspace_grid)
        self.grid_layout.setSpacing(12)
        ws_layout.addWidget(self.workspace_grid)
        
        btn_new_ws = PushButton("新建工作区", workspace_card)
        btn_new_ws.clicked.connect(self.create_workspace)
        ws_layout.addWidget(btn_new_ws)
        
        layout.addWidget(workspace_card)
        
        # 进入工作区按钮
        btn_enter = PrimaryPushButton("进入工作区", self)
        btn_enter.clicked.connect(self.enter_workspace)
        layout.addWidget(btn_enter)
        
        layout.addStretch()
    
    def show_project(self, project: Project):
        """显示项目信息"""
        self.current_project = project
        self.selected_workspace = None
        
        if not project:
            self._clear_project_info()
            return
        
        print(f"[操作] 显示项目详情: {project.name}, 工作区数量={len(project.workspaces)}")
        
        self.name_label.setText(project.name)
        self.desc_label.setText(project.desc or "无描述")
        self.time_label.setText(f"创建时间: {format_datetime(project.created_at)}")
        self.path_label.setText(f"项目路径: {project.path}")
        
        self._load_workspaces(project.workspaces)
    
    def _clear_project_info(self):
        """清空项目信息显示"""
        print("[操作] 清空项目详情显示")
        self.name_label.setText("")
        self.desc_label.setText("")
        self.time_label.setText("")
        self.path_label.setText("")
        self._clear_workspaces()
    
    def _load_workspaces(self, workspaces):
        """加载工作区列表"""
        self._clear_workspaces()
        
        for i, workspace in enumerate(workspaces):
            row = i // 3
            col = i % 3
            card = self._create_workspace_card(workspace)
            self.grid_layout.addWidget(card, row, col)
    
    def _clear_workspaces(self):
        """清空工作区列表"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _create_workspace_card(self, workspace):
        """创建工作区卡片"""
        card = SimpleCardWidget(self.workspace_grid)
        card.setFixedSize(200, 120)
        
        layout = VBoxLayout(card)
        
        name = BodyLabel(workspace.name, card)
        name.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(name)
        
        layout.addStretch()
        
        btn = PushButton("进入", card)
        btn.clicked.connect(lambda: self._on_workspace_clicked(workspace))
        layout.addWidget(btn)
        
        return card
    
    def _on_workspace_clicked(self, workspace):
        """工作区点击处理"""
        self.selected_workspace = workspace
    
    def create_workspace(self):
        """创建工作区"""
        if not self.current_project:
            print("[操作] 创建工作区失败: 未选择项目")
            QMessageBox.warning(self, "错误", "请先选择项目")
            return
        
        name, ok = QInputDialog.getText(self, "新建工作区", "工作区名称:")
        if not ok or not name.strip():
            print("[操作] 取消创建工作区")
            return
        
        if self.main_window:
            workspace = self.main_window.create_workspace(self.current_project, name.strip())
            if workspace:
                self.show_project(self.current_project)
    
    def enter_workspace(self):
        """进入工作区"""
        if not self.current_project:
            QMessageBox.warning(self, "错误", "请先选择项目")
            return
        
        workspace = self.selected_workspace
        if not workspace:
            if self.current_project.workspaces:
                workspace = self.current_project.workspaces[0]
            else:
                QMessageBox.warning(self, "错误", "请先创建工作区")
                return
        
        if self.main_window:
            self.main_window.show_workspace(self.current_project, workspace)


class ProjectCenterWidget(QWidget):
    """项目中心主组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 项目列表侧边栏
        self.project_list = ProjectListWidget(self)
        self.project_list.setFixedWidth(300)
        self.project_list.main_window = self.main_window
        layout.addWidget(self.project_list)
        
        # 项目详情面板
        self.project_detail = ProjectDetailWidget(self)
        self.project_detail.main_window = self.main_window
        layout.addWidget(self.project_detail, stretch=1)
    
    def refresh(self):
        """刷新项目列表"""
        print("[操作] 刷新项目中心")
        if self.main_window:
            projects = self.main_window.get_projects()
            self.project_list.load_projects(projects)
