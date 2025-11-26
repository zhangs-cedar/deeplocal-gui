# Gradio 风格 PyQt6 组件库架构设计

## 设计目标

基于 PyQt6 实现类似 Gradio 的组件库，支持使用 `with` 语句构建页面，API 风格与 Gradio 保持一致。

## 核心设计原则（Linus 风格）

1. **直接调用**：组件间通过 parent 引用直接调用方法
2. **无消息总线**：不使用 pubsub，避免间接调用
3. **简洁 API**：使用 `with` 语句提供优雅的 API
4. **清晰结构**：每个组件职责单一，边界清晰
5. **最小依赖**：只使用 PyQt6，不引入额外框架

## 架构设计

### 1. 上下文管理系统

#### 全局上下文栈
```python
_context_stack: List[QWidget] = []
```

**设计说明**：
- 使用模块级全局栈管理 `with` 语句的嵌套
- 在实际使用中，通常只有一个组件树，全局栈是安全的
- 如果需要在多个独立组件树中使用，可以考虑将栈作为 `GradioBlocks` 的实例属性

#### 上下文管理器混入类
```python
class _ContextMixin:
    """上下文管理器混入类"""
    def __enter__(self):
        _context_stack.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if _context_stack and _context_stack[-1] is self:
            _context_stack.pop()
        return False
```

### 2. 自动组件添加机制

```python
def _auto_add_to_context(widget: QWidget):
    """自动将组件添加到当前上下文（Linus 风格：直接调用）"""
    if widget.parent():
        return
    
    current = _get_current_context()
    if not current:
        return
    
    # 直接调用父组件方法，无间接调用
    if isinstance(current, GradioTabs) and isinstance(widget, GradioTab):
        current.addTab(widget)
    elif isinstance(current, GradioTab):
        current.addWidget(widget)
    elif isinstance(current, GradioRow):
        stretch = widget.get_scale() if isinstance(widget, GradioColumn) else 0
        current.addWidget(widget, stretch)
    elif isinstance(current, (GradioColumn, GradioGroup, GradioBlocks, GradioFlow)):
        current.addWidget(widget)
```

### 3. 组件层次结构

```
GradioBlocks (根容器)
├── GradioRow (水平布局)
│   ├── GradioColumn (垂直布局)
│   │   └── 各种组件 (Button, Card, etc.)
│   └── GradioColumn
├── GradioFlow (流式布局)
│   └── 各种组件
├── GradioTabs (标签页)
│   └── GradioTab
│       └── 各种组件
└── GradioGroup (分组容器)
    └── 各种组件
```

### 4. 主题系统

#### 主题查找机制
```python
def _get_theme(widget: QWidget) -> GradioTheme:
    """从组件树向上查找主题（直接调用，无全局状态）"""
    current = widget
    while current:
        if isinstance(current, GradioBlocks):
            return current._theme
        current = current.parent()
    return GradioTheme('light')  # 默认亮色主题
```

**设计说明**：
- 通过组件树向上查找，符合 Linus 风格的"直接调用"原则
- 每个 `GradioBlocks` 实例维护自己的主题
- 子组件通过 parent 链直接访问主题

## API 设计

### 基本用法

```python
from component import GradioBlocks, GradioRow, GradioButton

# 创建应用
demo = GradioBlocks(theme='light')

# 使用 with 语句构建页面
with demo:
    with GradioRow():
        btn0 = GradioButton("Button 0", scale=0)
        btn1 = GradioButton("Button 1", scale=1)
        btn2 = GradioButton("Button 2", scale=2)
```

### 组件自动添加

在 `with` 语句块中创建的组件会自动添加到当前上下文：

```python
with demo:
    with GradioRow():
        # 这些按钮会自动添加到 Row
        GradioButton("Button 1")
        GradioButton("Button 2")
        GradioButton("Button 3")
```

### Scale 参数支持

`GradioColumn` 支持 `scale` 参数，用于控制相对大小：

```python
with GradioRow():
    col1 = GradioColumn(scale=1)  # 占据 1 份空间
    col2 = GradioColumn(scale=2)  # 占据 2 份空间（是 col1 的 2 倍）
```

## 组件设计

### 1. GradioBlocks

**职责**：
- 根容器，管理主题
- 提供滚动支持
- 管理子组件

**关键方法**：
- `addWidget(widget)`: 添加子组件
- `toggle_theme()`: 切换主题
- `get_theme()`: 获取主题

### 2. GradioRow

**职责**：
- 水平布局容器
- 支持 `scale` 参数（通过 `GradioColumn`）

**关键方法**：
- `addWidget(widget, stretch=0)`: 添加子组件，支持 stretch

### 3. GradioColumn

**职责**：
- 垂直布局容器
- 支持 `scale` 参数

**关键方法**：
- `addWidget(widget)`: 添加子组件
- `get_scale()`: 获取 scale 值

### 4. GradioFlow

**职责**：
- 流式布局，支持自动换行
- 类似 CSS flexbox 的 wrap 效果

**关键方法**：
- `addWidget(widget)`: 添加子组件

### 5. GradioButton

**职责**：
- 按钮组件
- 支持多种 variant 和 size

**关键属性**：
- `variant`: 'primary', 'secondary', 'stop', 'huggingface'
- `size`: 'sm', 'md', 'lg'

## 使用示例

### 示例 1：基本布局

```python
from component import GradioBlocks, GradioRow, GradioColumn, GradioButton

demo = GradioBlocks(theme='light')
with demo:
    with GradioRow():
        btn0 = GradioButton("Button 0")
        btn1 = GradioButton("Button 1")
        btn2 = GradioButton("Button 2")
```

### 示例 2：Scale 参数

```python
demo = GradioBlocks(theme='light')
with demo:
    with GradioRow():
        col1 = GradioColumn(scale=1)
        with col1:
            GradioButton("Button 1")
        
        col2 = GradioColumn(scale=2)
        with col2:
            GradioButton("Button 2")
```

### 示例 3：嵌套布局

```python
demo = GradioBlocks(theme='light')
with demo:
    with GradioRow():
        with GradioColumn(scale=1):
            GradioButton("Left")
        
        with GradioColumn(scale=2):
            with GradioRow():
                GradioButton("Top")
                GradioButton("Bottom")
```

## 实现细节

### 1. 上下文栈管理

- 使用全局栈 `_context_stack` 管理 `with` 语句的嵌套
- 每个支持 `with` 语句的组件都混入 `_ContextMixin`
- 进入 `with` 块时，组件被推入栈
- 退出 `with` 块时，组件从栈中弹出

### 2. 组件自动添加

- 组件初始化时，如果没有指定 `parent`，会调用 `_auto_add_to_context`
- `_auto_add_to_context` 检查当前上下文栈，将组件添加到合适的父组件
- 根据父组件类型，调用相应的 `addWidget` 或 `addTab` 方法

### 3. 主题传播

- 主题存储在 `GradioBlocks` 实例中
- 子组件通过 `_get_theme` 函数向上查找主题
- 主题切换时，递归更新所有子组件的样式

## 优势

1. **API 优雅**：使用 `with` 语句，代码结构清晰
2. **自动管理**：组件自动添加到正确的父容器
3. **直接调用**：符合 Linus 风格，无间接调用
4. **类型安全**：使用类型提示，IDE 支持良好
5. **易于扩展**：新组件只需混入 `_ContextMixin` 即可支持 `with` 语句

## 注意事项

1. **全局上下文栈**：在大多数场景下是安全的，但如果需要多个独立的组件树，需要考虑使用实例属性
2. **组件生命周期**：组件在 `with` 块中创建后，会自动添加到父容器
3. **主题管理**：主题通过组件树向上查找，确保一致性

