from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json
import uuid


@dataclass
class Workspace:
    id: str
    name: str
    project_id: str
    created_at: datetime
    path: Path
    datasets: List[dict] = field(default_factory=list)
    experiments: List[dict] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict, project_path: Path):
        workspace_path = project_path / "workspaces" / data["id"]
        return cls(
            id=data["id"],
            name=data["name"],
            project_id=data["project_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            path=workspace_path
        )


@dataclass
class Project:
    id: str
    name: str
    desc: str
    created_at: datetime
    path: Path
    workspaces: List[Workspace] = field(default_factory=list)
    
    def add_workspace(self, workspace: Workspace):
        self.workspaces.append(workspace)
    
    def remove_workspace(self, workspace_id: str):
        before_count = len(self.workspaces)
        self.workspaces = [w for w in self.workspaces if w.id != workspace_id]
        after_count = len(self.workspaces)
        if before_count != after_count:
            print(f"[操作] 删除工作区: project={self.name}, workspace_id={workspace_id}")
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        for w in self.workspaces:
            if w.id == workspace_id:
                return w
        return None
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "created_at": self.created_at.isoformat(),
            "path": str(self.path),
            "workspaces": [w.to_dict() for w in self.workspaces]
        }
    
    @classmethod
    def from_dict(cls, data: dict, project_path: Path):
        project = cls(
            id=data["id"],
            name=data["name"],
            desc=data.get("desc", ""),
            created_at=datetime.fromisoformat(data["created_at"]),
            path=project_path
        )
        for w_data in data.get("workspaces", []):
            workspace = Workspace.from_dict(w_data, project.path)
            project.workspaces.append(workspace)
        return project
    
    def save(self):
        project_file = self.path / "project.json"
        project_file.parent.mkdir(parents=True, exist_ok=True)
        with open(project_file, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"[操作] 保存项目: {self.name} -> {project_file}")
    
    @classmethod
    def load(cls, project_path: Path):
        project_file = project_path / "project.json"
        if not project_file.exists():
            print(f"[操作] 加载项目失败: 文件不存在 {project_file}")
            return None
        with open(project_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        project = cls.from_dict(data, project_path)
        print(f"[操作] 加载项目: {project.name} from {project_file}")
        return project

