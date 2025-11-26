"""
Gradio 风格组件库
按照 Linus 风格设计：简洁、直接、清晰
"""
from component.gradio import (
    GradioTheme,
    GradioBlocks,
    GradioRow,
    GradioColumn,
    GradioGroup,
    GradioTabs,
    GradioTab,
    GradioButton,
    GradioFlow,
    GradioFlowLayout,
    GradioThemeToggleButton,
    _get_theme,
)
# 卡片组件
from component.card import GradioCard

# 向后兼容别名
Card = GradioCard

__all__ = [
    # 主题
    'GradioTheme',
    '_get_theme',
    # 布局组件
    'GradioBlocks',
    'GradioRow',
    'GradioColumn',
    'GradioGroup',
    'GradioFlow',
    'GradioFlowLayout',
    # 标签页
    'GradioTabs',
    'GradioTab',
    # 按钮
    'GradioButton',
    'GradioThemeToggleButton',
    # 卡片
    'GradioCard',
    'Card',
]
