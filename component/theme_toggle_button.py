from .button import Button
from .blocks import Blocks


class ThemeToggleButton(Button):
    def __init__(self, blocks: Blocks = None, parent=None):
        # 初始化主题切换按钮，自动查找或使用传入的 Blocks 实例
        super().__init__("", 'secondary', parent)
        if blocks:
            self._blocks = blocks
        else:
            current = self.parent()
            while current:
                if isinstance(current, Blocks):
                    self._blocks = current
                    break
                current = current.parent()
            else:
                raise ValueError("需要 Blocks 实例")
        
        self.clicked_signal.connect(self._toggle)
        self._update_text()
    
    def _update_text(self):
        # 根据当前主题更新按钮文本
        if self._blocks._theme.mode == 'light':
            self.setText("🌙")
        else:
            self.setText("☀️")
    
    def _toggle(self):
        # 切换主题并更新按钮文本
        self._blocks.toggle_theme()
        self._update_text()
