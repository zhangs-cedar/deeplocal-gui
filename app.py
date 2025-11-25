import sys
import os
from PyQt6.QtWidgets import QApplication
from app_ui.main_window import MainWindow
from cedar.utils import print,load_config

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'app.yaml')
os.environ['CONFIG_FILE'] = CONFIG_FILE
cfg = load_config()
os.environ['LOG_PATH'] = os.path.join(cfg["project_dir"],"logs", 'app.log')

print(f"LOG_PATH: {os.environ['LOG_PATH']}")
print("[启动] 初始化应用...")
print(f"[配置] 项目目录: {cfg['project_dir']}")
print(f"[配置] 日志路径: {os.environ['LOG_PATH']}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("[启动] 应用启动完成")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

