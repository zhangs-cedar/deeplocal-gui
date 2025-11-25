import sys
import os
from PyQt6.QtWidgets import QApplication
from app_ui.main_window import MainWindow
from config import get_config
from cedar.utils import print


def main():
    config = get_config()
    os.environ['LOG_PATH'] = str(config.get_log_path())
    
    print(f"LOG_PATH: {os.environ['LOG_PATH']}")
    print("[启动] 初始化应用...")
    print(f"[配置] 项目目录: {config.get_projects_dir()}")
    print(f"[配置] 日志路径: {config.get_log_path()}")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("[启动] 应用启动完成")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

