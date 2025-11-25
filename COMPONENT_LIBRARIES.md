# PyQt6 组件库推荐

PyQt6 本身比较底层，但有很多优秀的第三方组件库可以大大简化开发：

## 1. qfluentwidgets (推荐 ⭐⭐⭐⭐⭐)

**最流行的 PyQt6 组件库，提供 Fluent Design 风格的现代化组件**

### 安装
```bash
pip install qfluentwidgets
```

### 特点
- 🎨 现代化的 Fluent Design 风格
- 📦 丰富的预定义组件（卡片、按钮、导航栏等）
- 🎯 开箱即用，减少大量样板代码
- 📱 响应式设计支持
- 🌈 主题切换支持

### 示例对比

**传统方式（当前代码）：**
```python
# 需要手动创建卡片、设置样式、绑定事件
card = QFrame()
card.setObjectName("project_card")
card.setCursor(Qt.CursorShape.PointingHandCursor)
layout = QVBoxLayout(card)
layout.setContentsMargins(16, 16, 16, 16)
name = QLabel(project.name)
name.setObjectName("project_name")
layout.addWidget(name)
# ... 更多代码
```

**使用 qfluentwidgets：**
```python
from qfluentwidgets import CardWidget, BodyLabel, CaptionLabel

card = CardWidget()
card.setFixedSize(280, 120)
name = BodyLabel(project.name, card)
desc = CaptionLabel(project.desc or "无描述", card)
card.vBoxLayout.addWidget(name)
card.vBoxLayout.addWidget(desc)
card.clicked.connect(lambda: self._on_card_clicked(project))
```

## 2. PyQt6-Material

**Material Design 风格的组件库**

### 安装
```bash
pip install PyQt6-Material
```

### 特点
- 🎨 Google Material Design 风格
- 🎯 简洁的 API
- 📦 常用组件封装

## 3. qtawesome

**图标库，简化图标使用**

### 安装
```bash
pip install qtawesome
```

### 示例
```python
import qtawesome as qta

# 使用图标
icon = qta.icon('fa5s.folder', color='blue')
button.setIcon(icon)
```

## 4. Qt Designer (官方工具)

**可视化界面设计工具**

### 安装
```bash
pip install PyQt6-tools
```

### 使用
```bash
# 启动设计器
designer

# 将 .ui 文件转换为 Python 代码
pyuic6 your_ui_file.ui -o your_python_file.py
```

## 推荐方案

**对于你的项目，推荐使用 `qfluentwidgets`：**

1. ✅ 最活跃维护
2. ✅ 文档完善
3. ✅ 组件丰富
4. ✅ 代码简洁
5. ✅ 样式现代化

### 快速开始

```bash
pip install qfluentwidgets
```

然后可以这样简化代码：

```python
from qfluentwidgets import (
    CardWidget, BodyLabel, CaptionLabel, 
    PrimaryPushButton, FluentWindow,
    NavigationInterface, NavigationItemPosition
)

# 创建卡片（一行代码）
card = CardWidget(parent)
card.setFixedSize(280, 120)

# 创建按钮（自动样式）
btn = PrimaryPushButton("新建项目", self)

# 创建导航栏（自动布局）
navigation = NavigationInterface(self)
navigation.addItem("project", "项目中心", icon="folder")
```

## 迁移建议

1. **渐进式迁移**：可以先在新功能中使用组件库
2. **保持兼容**：组件库的组件都是 PyQt6 组件的子类，可以混用
3. **减少样式代码**：使用组件库后，`styles.py` 可以大幅简化

