# 贡献指南

感谢你对PyInstaller GUI构建器项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 Bug报告
- 💡 功能建议
- 📝 文档改进
- 🔧 代码贡献
- 🌍 国际化翻译

## 🤝 如何贡献

### 报告问题

如果你发现了bug或有功能建议，请：

1. 首先搜索[现有issues](https://github.com/yourusername/pyinstaller-gui/issues)，确保问题未被报告过
2. 使用相应的issue模板创建新issue：
   - [Bug报告](https://github.com/yourusername/pyinstaller-gui/issues/new?template=bug_report.yml)
   - [功能请求](https://github.com/yourusername/pyinstaller-gui/issues/new?template=feature_request.yml)
   - [问题咨询](https://github.com/yourusername/pyinstaller-gui/issues/new?template=question.yml)

### 提交代码

#### 开发环境搭建

1. **Fork项目**
   ```bash
   # 在GitHub上Fork项目，然后克隆你的Fork
   git clone https://github.com/yourusername/pyinstaller-gui.git
   cd pyinstaller-gui
   ```

2. **创建开发环境**
   ```bash
   # 建议使用虚拟环境
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # 安装依赖
   pip install -r requirements.txt
   ```

3. **验证环境**
   ```bash
   # 运行程序确保环境正常
   python pyinstaller_gui_pyside6.py
   ```

#### 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或者 bug 修复分支
   git checkout -b fix/your-bug-fix
   ```

2. **进行开发**
   - 保持代码风格一致
   - 添加必要的注释
   - 确保功能完整性

3. **测试验证**
   ```bash
   # 运行程序测试
   python pyinstaller_gui_pyside6.py
   
   # 测试各项功能是否正常
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   # 或者 "fix: fix your bug description"
   ```

5. **推送并创建PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   然后在GitHub上创建Pull Request

## 📋 代码规范

### Python代码风格

- 遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)代码风格指南
- 使用4个空格缩进
- 行长度不超过88个字符
- 函数和类使用docstring文档
- 变量命名使用snake_case
- 类命名使用PascalCase

### 注释规范

```python
def example_function(param1: str, param2: int) -> bool:
    """
    函数功能简述
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
        
    Returns:
        返回值说明
    """
    # 具体实现注释
    pass
```

### PySide6特定规范

- 信号使用：`from PySide6.QtCore import Signal`
- 枚举访问：使用完整路径，如`QDialogButtonBox.StandardButton.Ok`
- 错误处理：处理可能为None的返回值

## 🏗️ 项目架构

### 主要组件

- `PyInstallerGUI`：主窗口类
- `create_*_tab()`：各标签页创建方法
- `add_*_file/directory()`：资源文件管理方法
- `generate_command()`：命令生成逻辑

### 添加新功能

1. **界面元素**：在相应的`create_*_tab()`方法中添加
2. **功能逻辑**：创建对应的处理方法
3. **数据存储**：在`__init__`中添加必要的数据属性
4. **命令生成**：在`generate_command()`中添加对应逻辑

### 修改现有功能

1. 确保向后兼容性
2. 保持界面一致性
3. 更新相关文档

## 🧪 测试指南

### 手动测试

在提交PR之前，请确保以下功能正常：

- [ ] 程序能正常启动并显示界面
- [ ] 各个标签页切换正常
- [ ] 文件/目录选择功能正常
- [ ] 命令生成功能正确
- [ ] 复制到剪贴板功能正常
- [ ] 图标处理功能正常
- [ ] 各项设置保存和重置功能正常

### 测试用例

1. **基本功能测试**
   - 选择Python脚本文件
   - 配置各项选项
   - 生成PyInstaller命令
   - 复制命令到剪贴板

2. **边缘情况测试**
   - 无效文件路径处理
   - 空配置项处理
   - 特殊字符处理

3. **界面交互测试**
   - 响应式布局
   - 按钮状态变化
   - 工具提示显示

## 📝 文档贡献

### 文档类型

- **用户文档**：README.md、使用指南
- **开发文档**：代码注释、API文档
- **项目文档**：CHANGELOG.md、贡献指南

### 文档风格

- 使用清晰的标题结构
- 提供具体的示例代码
- 包含必要的截图说明
- 保持内容更新及时

## 🌍 国际化贡献

目前项目主要支持中文，我们欢迎以下语言的翻译贡献：

- 英文 (English)
- 日文 (日本語)
- 韩文 (한국어)
- 其他语言

## 📞 联系方式

如果你在贡献过程中有任何问题，可以通过以下方式联系：

- 创建[Discussion](https://github.com/yourusername/pyinstaller-gui/discussions)
- 提交[Issue](https://github.com/yourusername/pyinstaller-gui/issues)
- 发送邮件至：your-email@example.com

## 🎖️ 贡献者

感谢所有为这个项目做出贡献的开发者：

- [@username1](https://github.com/username1) - 主要开发者
- [@username2](https://github.com/username2) - 文档贡献者
- [@username3](https://github.com/username3) - 测试贡献者

更多贡献者请查看[Contributors页面](https://github.com/yourusername/pyinstaller-gui/graphs/contributors)。

---

再次感谢你的贡献！你的帮助让这个项目变得更好！ 🚀