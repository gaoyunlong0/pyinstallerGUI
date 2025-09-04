# PyInstaller GUI 构建器

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

一个基于PySide6的现代化PyInstaller GUI工具，提供直观的图形界面来配置和生成PyInstaller命令，简化Python应用程序的打包过程。

## ✨ 主要特性

- 🎨 **现代化界面**: 采用PySide6设计的简洁美观界面
- 🔧 **完整配置**: 支持PyInstaller的所有主要选项配置
- 📦 **资源管理**: 便捷的数据文件和二进制文件管理
- 🔍 **模块管理**: 智能的模块导入和排除管理
- 🎯 **双图标机制**: 支持窗口图标和可执行文件图标分别设置
- 📋 **命令生成**: 一键生成并复制PyInstaller命令
- 🖱️ **拖放支持**: 支持文件、文件夹和文本的拖放操作
- 🌍 **跨平台**: 支持Windows、macOS和Linux系统

## 📸 界面截图

### 主界面
![主界面]([https://via.placeholder.com/800x600/f8f9fa/333333?text=PyInstaller+GUI+%E4%B8%BB%E7%95%8C%E9%9D%A2](https://github.com/gaoyunlong0/pyinstallerGUI/blob/main/img/1b815815-e350-4356-9c70-5bdece2c3138.png?raw=true))



### 功能特色
- **基本设置**: 脚本选择、生成模式、窗口模式、图标设置等
- **模块管理**: 常用模块快速选择、隐藏导入、排除模块配置
- **资源文件**: 数据文件和二进制文件的添加管理
- **高级设置**: 调试选项、加密设置、启动画面等

## 🚀 快速开始

### 环境要求

- Python 3.7+
- PySide6
- PIL/Pillow (用于图标转换)

### 安装依赖

```bash
pip install PySide6 Pillow pyinstaller
```

或使用requirements文件：

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python pyinstaller_gui_pyside6.py
```

或者在Windows系统上双击运行：
```
启动PyInstaller_GUI.bat
```

## 📖 使用指南

### 基本使用流程

1. **选择脚本文件**: 点击"浏览"按钮或直接拖放Python脚本文件到输入框
2. **配置选项**: 在各个标签页中配置打包选项
   - **基本设置**: 选择生成模式、窗口模式、设置图标等
   - **模块管理**: 添加隐藏导入模块、排除不需要的模块
   - **资源文件**: 添加数据文件和二进制文件
   - **高级设置**: 配置调试选项、加密等高级功能
3. **生成命令**: 点击"生成命令"按钮
4. **复制执行**: 点击"复制命令"将命令复制到剪贴板
5. **手动执行**: 在终端中粘贴并执行命令

### 拖放功能说明

程序支持多种拖放操作，提高使用效率：

- **脚本文件**: 将Python脚本文件拖放到脚本输入框中
- **图标文件**: 将图片文件拖放到图标输入框中（支持ico、png、jpg、bmp、gif格式）
- **目录路径**: 将文件夹拖放到输出目录或工作目录输入框中
- **启动画面**: 将图片文件拖放到启动画面输入框中
- **文本输入**: 将文本拖放到程序名称、模块名称等文本输入框中
- **资源文件**: 将文件或目录拖放到资源文件区域，自动判断并添加为数据文件或二进制文件

所有拖放操作都支持直观的视觉反馈，当文件类型符合要求时会高亮显示。

### 双图标机制说明

- **icon.ico**: 用于程序运行时的窗口显示图标
- **icon1.ico**: 用于PyInstaller打包后的可执行文件图标（任务栏显示）

程序会自动处理图标转换和管理，支持多种图片格式输入。

### 常用模块快速添加

程序内置了常用Python模块的分类选择：
- 🤖 人工智能/机器学习: tensorflow, torch, sklearn等
- 📈 数据处理: numpy, pandas, matplotlib等
- 🖌️ GUI框架: tkinter, PyQt5/6, PySide2/6等
- 🌍 网络/API: requests, flask, fastapi等

### 减小打包体积

PyInstaller打包的可执行文件可能会比较大，可以通过以下方式减小体积：

1. **排除不必要的模块**：在"模块管理"标签页中使用"排除模块"功能，排除不需要的模块
2. **使用目录模式**：相比单文件模式，目录模式通常生成更小的文件
3. **启用UPX压缩**：默认启用UPX压缩，可以显著减小文件大小
4. **排除特定模块的UPX压缩**：某些模块（如numpy、scipy）使用UPX压缩可能导致问题，可以在"高级设置"中排除这些模块
5. **移除符号表**：在Linux/macOS系统上，可以使用"--strip"选项移除符号表减小体积
6. **精简资源文件**：只添加必要的资源文件，避免包含不必要的数据文件

在"高级设置"标签页中，我们提供了专门的优化选项：
- **移除符号表**：适用于Linux/macOS系统的选项，可以减小可执行文件大小
- **UPX排除模块**：指定不使用UPX压缩的模块，避免某些模块因UPX压缩而出现问题

## 🛠️ 开发环境搭建

### 克隆项目
```bash
git clone https://github.com/yourusername/pyinstaller-gui.git
cd pyinstaller-gui
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行开发版本
```bash
python pyinstaller_gui_pyside6.py
```

## 📁 项目结构

```
pyinstaller-gui/
├── pyinstaller_gui_pyside6.py    # 主程序文件
├── icon.ico                      # 应用程序图标
├── requirements.txt              # Python依赖文件
├── README.md                     # 项目说明文档
├── LICENSE                       # 开源许可证
├── CHANGELOG.md                  # 版本更新日志
├── CONTRIBUTING.md               # 贡献指南
├── SECURITY.md                   # 安全政策
├── .gitignore                    # Git忽略文件
└── .github/                      # GitHub配置
    ├── workflows/                # GitHub Actions工作流
    │   ├── ci.yml               # 持续集成
    │   └── release.yml          # 自动发布
    └── ISSUE_TEMPLATE/          # Issue模板
        ├── bug_report.yml       # Bug报告模板
        ├── feature_request.yml  # 功能请求模板
        └── question.yml         # 问题咨询模板
```

## 🔧 配置选项说明

### 基本设置
- **脚本文件**: 要打包的主Python文件
- **生成模式**: 单文件(-F) 或 目录模式(-D)
- **窗口模式**: 控制台模式(-c) 或 窗口模式(-w)
- **图标文件**: 可执行文件的图标
- **程序名称**: 生成的可执行文件名称

### 高级选项
- **输出目录**: 指定打包输出目录
- **工作目录**: 指定临时工作目录
- **搜索路径**: 额外的模块搜索路径
- **调试模式**: 启用详细调试信息
- **UPX压缩**: 启用/禁用UPX压缩
- **优化选项**: 减小可执行文件体积的选项，包括移除符号表和UPX排除模块

## 🤝 贡献指南

欢迎提交问题和功能请求！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 开发指南
1. Fork 这个项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🐛 问题报告

如果遇到问题，请通过以下方式报告：
1. 查看 [已知问题](https://github.com/yourusername/pyinstaller-gui/issues)
2. 创建新的 [Issue](https://github.com/yourusername/pyinstaller-gui/issues/new/choose)
3. 提供详细的错误信息和复现步骤

## 🔗 相关链接

- [PyInstaller官方文档](https://pyinstaller.readthedocs.io/)
- [PySide6官方文档](https://doc.qt.io/qtforpython/)
- [Python官方网站](https://www.python.org/)

## ⭐ 致谢

感谢所有为这个项目做出贡献的开发者！

如果这个项目对你有帮助，请给它一个星标 ⭐

---


**注意**: 本工具仅生成PyInstaller命令，实际的打包执行需要在终端中手动运行生成的命令。
