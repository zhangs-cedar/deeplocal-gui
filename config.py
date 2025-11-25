#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
from pathlib import Path
from typing import Optional


class Config:
    _instance: Optional['Config'] = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.config_file = self._find_config_file()
        self._load_config()
    
    def _find_config_file(self) -> Path:
        current_dir = Path(__file__).parent
        config_file = current_dir / "app.yaml"
        if config_file.exists():
            return config_file
        return config_file
    
    def _load_config(self):
        if not self.config_file.exists():
            self._create_default_config()
        
        with open(self.config_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        
        self.project_dir = self._expand_path(data.get("project_dir", "~/.deeplocal-gui/projects"))
        self.log_path = self._expand_path(data.get("log_path", "~/.deeplocal-gui/app.log"))
        self.window_title = data.get("window_title", "深度学习训练工具")
        self.window_width = data.get("window_width", 1200)
        self.window_height = data.get("window_height", 800)
    
    def _expand_path(self, path: str) -> Path:
        expanded = os.path.expanduser(path)
        expanded = os.path.expandvars(expanded)
        return Path(expanded)
    
    def _create_default_config(self):
        default_config = {
            "project_dir": "~/.deeplocal-gui/projects",
            "log_path": "~/.deeplocal-gui/app.log",
            "window_title": "深度学习训练工具",
            "window_width": 1200,
            "window_height": 800
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)
    
    def get_projects_dir(self) -> Path:
        dir_path = self.project_dir
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def get_log_path(self) -> Path:
        log_path = self.log_path
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return log_path


def get_config() -> Config:
    return Config()

