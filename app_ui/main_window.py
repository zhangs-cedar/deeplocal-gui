from PyQt6.QtWidgets import QMainWindow
from datetime import datetime
from pathlib import Path
from app_ui.models import Project, Workspace

from app_ui.project_center import ProjectCenterWidget
from utils.utils import generate_id, format_datetime
from cedar.utils import print, load_config


class MainWindow(QMainWindow):
    """主窗口 - Linux 风格，使用原生 PyQt6"""
    
    def __init__(self):
        super().__init__()
        config = load_config()
        self.setWindowTitle(config['window_title'])
        self.resize(config['window_width'], config['window_height'])
        self.current_project = None
        self.current_workspace = None
        self.projects_dir = Path(config['project_dir'])
        print(f"[启动] 主窗口初始化，项目目录: {self.projects_dir}")
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建项目中心页面
        self.project_center = ProjectCenterWidget(self)
        self.setCentralWidget(self.project_center)
        
        # 刷新项目列表
        self.project_center.refresh()
    
    def get_projects(self) -> list:
        """获取所有项目列表"""
        print(f"[操作] 加载项目列表: {self.projects_dir}")
        projects = []
        if not self.projects_dir.exists():
            print(f"[操作] 项目目录不存在，返回空列表")
            return projects
        
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir():
                project = Project.load(project_dir)
                if project:
                    projects.append(project)
        
        result = sorted(projects, key=lambda p: p.created_at, reverse=True)
        print(f"[操作] 加载完成，共 {len(result)} 个项目")
        return result
    
    def create_project(self, name: str, desc: str = "") -> Project:
        """创建新项目"""
        print(f"[操作] 创建项目: name={name}, desc={desc}")
        project_id = generate_id()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_folder_name = f"project_{timestamp}"
        project_path = self.projects_dir / project_folder_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        project = Project(
            id=project_id,
            name=name,
            desc=desc,
            created_at=datetime.now(),
            path=project_path
        )
        
        self.create_workspace(project, "默认工作区", auto_save=False)
        project.save()
        self._create_project_readme(project)
        print(f"[操作] 项目创建成功: id={project_id}, path={project_path}")
        return project
    
    def _create_project_readme(self, project: Project):
        """创建项目 README 文件"""
        readme_path = project.path / "README.md"
        readme_content = f"""# {project.name}

## 项目信息

- **项目ID**: {project.id}
- **项目名称**: {project.name}
- **项目描述**: {project.desc}
- **创建时间**: {project.created_at.strftime("%Y-%m-%d %H:%M:%S")}
- **项目路径**: {project.path}

## 工作区列表

"""
        for i, workspace in enumerate(project.workspaces, 1):
            readme_content += f"{i}. {workspace.name} (ID: {workspace.id})\n"
        
        readme_content += f"""
## 说明

此项目由 deeplocal-gui 创建和管理。
项目配置文件: `project.json`
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"[操作] 创建项目 README: {readme_path}")
    
    def create_workspace(self, project: Project, name: str, auto_save: bool = True) -> Workspace:
        """创建工作区"""
        print(f"[操作] 创建工作区: project={project.name}, name={name}, auto_save={auto_save}")
        workspace_id = generate_id()
        workspace_path = project.path / "workspaces" / workspace_id
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        workspace = Workspace(
            id=workspace_id,
            name=name,
            project_id=project.id,
            created_at=datetime.now(),
            path=workspace_path
        )
        
        project.add_workspace(workspace)
        if auto_save:
            project.save()
        
        print(f"[操作] 工作区创建成功: id={workspace_id}, path={workspace_path}")
        return workspace
    
    def show_project_detail(self, project: Project):
        """显示项目详情"""
        print(f"[操作] 显示项目详情: {project.name} (id={project.id})")
        self.current_project = project
        self.project_center.project_detail.show_project(project)
    
    def show_workspace(self, project: Project, workspace: Workspace):
        """进入工作区"""
        print(f"[操作] 进入工作区: project={project.name}, workspace={workspace.name} (id={workspace.id})")
        self.current_project = project
        self.current_workspace = workspace
