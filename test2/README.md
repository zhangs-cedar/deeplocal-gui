# Gradio 风格 PyQt6 组件库

基于 PyQt6 实现的类似 Gradio 的组件库，支持使用 `with` 语句构建页面。

## 快速开始

### 基本用法

```python
from component import GradioBlocks, GradioRow, GradioButton

# 创建应用
demo = GradioBlocks(theme='light')

# 使用 with 语句构建页面
with demo:
    with GradioRow():
        btn0 = GradioButton("Button 0")
        btn1 = GradioButton("Button 1")
        btn2 = GradioButton("Button 2")
```

### Scale 参数示例

```python
demo = GradioBlocks(theme='light')
with demo:
    with GradioRow():
        # scale=0: 不扩展，保持最小宽度
        col0 = GradioColumn(scale=0, min_width=150)
        with col0:
            GradioButton("Button 0", scale=0)
        
        # scale=1: 占据 1 份空间
        col1 = GradioColumn(scale=1, min_width=200)
        with col1:
            GradioButton("Button 1", scale=1)
        
        # scale=2: 占据 2 份空间（是 col1 的 2 倍）
        col2 = GradioColumn(scale=2, min_width=200)
        with col2:
            GradioButton("Button 2", scale=2)
```

## 运行示例

```bash
# 运行完整示例
python test2/example_gradio_style.py
```

## 架构设计

详细架构设计请参考 [ARCHITECTURE.md](./ARCHITECTURE.md)

## 核心特性

1. **with 语句支持**：类似 Gradio 的 API，使用 `with` 语句构建页面
2. **自动组件管理**：组件自动添加到正确的父容器
3. **Scale 参数**：支持相对大小控制
4. **主题系统**：支持亮色/暗色主题切换
5. **流式布局**：支持自动换行的流式布局
6. **标签页**：支持多标签页界面

## 组件列表

- `GradioBlocks`: 根容器
- `GradioRow`: 水平布局容器
- `GradioColumn`: 垂直布局容器（支持 scale）
- `GradioFlow`: 流式布局容器（自动换行）
- `GradioButton`: 按钮组件
- `GradioCard`: 卡片组件
- `GradioTabs`: 标签页容器
- `GradioTab`: 标签页
- `GradioThemeToggleButton`: 主题切换按钮

## 设计原则（Linus 风格）

1. **直接调用**：组件间通过 parent 引用直接调用方法
2. **无消息总线**：不使用 pubsub，避免间接调用
3. **简洁 API**：使用 `with` 语句提供优雅的 API
4. **清晰结构**：每个组件职责单一，边界清晰
5. **最小依赖**：只使用 PyQt6，不引入额外框架

