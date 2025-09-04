#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6版本的PyInstaller命令构建器
简洁现代化界面，保留完整功能
"""

import sys
import os
from pathlib import Path
from PIL import Image
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QTabWidget, QGroupBox, QLabel, QLineEdit, QPushButton, 
    QRadioButton, QCheckBox, QComboBox, QListWidget, QTextEdit, 
    QFileDialog, QMessageBox, QInputDialog, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDragEnterEvent, QDropEvent, QIcon, QPixmap, QPainter, QBrush, QColor


class PyInstallerGUI(QMainWindow):
    """主窗口类 - 简洁现代化设计保留完整功能"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyInstaller 命令构建器")
        self.setMinimumSize(1200, 800)
        
        # 设置应用程序图标
        self.set_application_icon()
        
        # 数据存储
        self.search_paths = []
        self.data_files = []
        self.binary_files = []
        self.hidden_imports = []
        self.exclude_modules = []
        
        # 初始化UPX排除模块列表
        self.upx_exclude_modules = []
        
        self.setup_ui()
        self.apply_styles()
        self.center_window()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("🚀 PyInstaller 命令构建器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
            }
        """)
        
        # 主内容区域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # 左侧配置区
        config_widget = self.create_config_panel()
        
        # 右侧命令区
        command_widget = self.create_command_panel()
        
        content_layout.addWidget(config_widget, 2)
        content_layout.addWidget(command_widget, 1)
        
        layout.addWidget(title_label)
        layout.addLayout(content_layout)
    
    def create_config_panel(self):
        """创建配置面板"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        config_widget = QWidget()
        layout = QVBoxLayout(config_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 基本设置标签页
        basic_tab = self.create_basic_tab()
        tab_widget.addTab(basic_tab, "🔧 基本设置")
        
        # 模块管理标签页
        module_tab = self.create_module_tab()
        tab_widget.addTab(module_tab, "📦 模块管理")
        
        # 资源文件标签页
        resource_tab = self.create_resource_tab()
        tab_widget.addTab(resource_tab, "📁 资源文件")
        
        # 高级设置标签页
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "⚙️ 高级设置")
        
        layout.addWidget(tab_widget)
        scroll_area.setWidget(config_widget)
        
        return scroll_area
    
    def create_basic_tab(self):
        """创建基本设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # 脚本文件选择
        script_group = QGroupBox("📄 脚本文件")
        script_layout = QVBoxLayout(script_group)
        
        script_input_layout = QHBoxLayout()
        self.script_edit = QLineEdit()
        self.script_edit.setPlaceholderText("选择要打包的Python脚本文件...")
        # 启用拖拽
        self.script_edit.setAcceptDrops(True)
        self.script_edit.dragEnterEvent = self.script_drag_enter_event
        self.script_edit.dropEvent = self.script_drop_event
        
        script_browse_btn = QPushButton("浏览")
        script_browse_btn.clicked.connect(self.browse_script)
        
        script_input_layout.addWidget(self.script_edit)
        script_input_layout.addWidget(script_browse_btn)
        script_layout.addLayout(script_input_layout)

        # 生成模式
        mode_group = QGroupBox("🏗️ 生成模式")
        mode_layout = QVBoxLayout(mode_group)
        
        self.onefile_radio = QRadioButton("单文件模式 (-F)")
        self.onedir_radio = QRadioButton("目录模式 (-D)")
        self.onedir_radio.setChecked(True)
        
        mode_layout.addWidget(self.onedir_radio)
        mode_layout.addWidget(self.onefile_radio)
        
        # 窗口模式
        window_group = QGroupBox("🖥️ 窗口模式")
        window_layout = QVBoxLayout(window_group)
        
        self.console_radio = QRadioButton("控制台模式 (-c)")
        self.windowed_radio = QRadioButton("窗口模式 (-w)")
        self.console_radio.setChecked(True)
        
        window_layout.addWidget(self.console_radio)
        window_layout.addWidget(self.windowed_radio)
        
        # 图标和名称
        icon_group = QGroupBox("🎨 图标和名称")
        icon_layout = QFormLayout(icon_group)
        
        # 图标文件
        icon_widget = QWidget()
        icon_widget_layout = QHBoxLayout(icon_widget)
        icon_widget_layout.setContentsMargins(0, 0, 0, 0)
        
        self.icon_edit = QLineEdit()
        self.icon_edit.setPlaceholderText("选择图标文件...")
        self.icon_edit.setToolTip("支持多种图片格式，自动转换为.ico格式并移动到项目根目录")
        # 启用拖拽
        self.icon_edit.setAcceptDrops(True)
        self.icon_edit.dragEnterEvent = lambda event: self.generic_drag_enter_event(event, ['ico', 'png', 'jpg', 'jpeg', 'bmp', 'gif'])
        self.icon_edit.dropEvent = lambda event: self.icon_drop_event(event)
        icon_browse_btn = QPushButton("浏览")
        icon_browse_btn.clicked.connect(self.browse_icon)
        icon_browse_btn.setToolTip("选择任意格式的图片文件，程序会自动处理")
        
        icon_widget_layout.addWidget(self.icon_edit)
        icon_widget_layout.addWidget(icon_browse_btn)
        
        # 程序名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("可执行文件名称（可选）")
        # 启用拖拽（文本拖拽）
        self.name_edit.setAcceptDrops(True)
        self.name_edit.dragEnterEvent = self.text_drag_enter_event
        self.name_edit.dropEvent = self.text_drop_event
        
        icon_layout.addRow("图标文件:", icon_widget)
        icon_layout.addRow("程序名称:", self.name_edit)
        
        # 路径设置
        path_group = QGroupBox("📂 路径设置")
        path_layout = QFormLayout(path_group)
        
        # 输出目录
        output_widget = QWidget()
        output_layout = QHBoxLayout(output_widget)
        output_layout.setContentsMargins(0, 0, 0, 0)
        
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("输出目录（默认: ./dist）")
        # 启用拖拽
        self.output_edit.setAcceptDrops(True)
        self.output_edit.dragEnterEvent = self.folder_drag_enter_event
        self.output_edit.dropEvent = lambda event: self.folder_drop_event(event, self.output_edit)
        output_browse_btn = QPushButton("浏览")
        output_browse_btn.clicked.connect(self.browse_output)
        
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_browse_btn)
        
        # 工作目录
        work_widget = QWidget()
        work_layout = QHBoxLayout(work_widget)
        work_layout.setContentsMargins(0, 0, 0, 0)
        
        self.work_edit = QLineEdit()
        self.work_edit.setPlaceholderText("工作目录（默认: ./build）")
        # 启用拖拽
        self.work_edit.setAcceptDrops(True)
        self.work_edit.dragEnterEvent = self.folder_drag_enter_event
        self.work_edit.dropEvent = lambda event: self.folder_drop_event(event, self.work_edit)
        work_browse_btn = QPushButton("浏览")
        work_browse_btn.clicked.connect(self.browse_work)
        
        work_layout.addWidget(self.work_edit)
        work_layout.addWidget(work_browse_btn)
        
        path_layout.addRow("输出目录:", output_widget)
        path_layout.addRow("工作目录:", work_widget)
        
        # 搜索路径
        search_group = QGroupBox("🔍 额外搜索路径")
        search_layout = QVBoxLayout(search_group)
        
        search_controls = QHBoxLayout()
        add_path_btn = QPushButton("添加路径")
        remove_path_btn = QPushButton("删除选中")
        add_path_btn.clicked.connect(self.add_search_path)
        remove_path_btn.clicked.connect(self.remove_search_path)
        
        search_controls.addWidget(add_path_btn)
        search_controls.addWidget(remove_path_btn)
        search_controls.addStretch()
        
        self.search_list = QListWidget()
        self.search_list.setMaximumHeight(80)
        
        search_layout.addLayout(search_controls)
        search_layout.addWidget(self.search_list)
        
        # 基本选项
        basic_options_group = QGroupBox("⚙️ 基本选项")
        basic_options_layout = QVBoxLayout(basic_options_group)
        
        self.clean_check = QCheckBox("清理缓存 (--clean)")
        self.noconfirm_check = QCheckBox("不询问直接覆盖 (-y)")
        self.uac_check = QCheckBox("请求管理员权限 (--uac-admin)")
        
        # 默认开启不询问直接覆盖
        self.noconfirm_check.setChecked(True)
        
        basic_options_layout.addWidget(self.clean_check)
        basic_options_layout.addWidget(self.noconfirm_check)
        basic_options_layout.addWidget(self.uac_check)
        
        # 添加到布局
        layout.addWidget(script_group)
        layout.addWidget(mode_group)
        layout.addWidget(window_group)
        layout.addWidget(icon_group)
        layout.addWidget(path_group)
        layout.addWidget(search_group)
        layout.addWidget(basic_options_group)
        layout.addStretch()
        
        return widget
    
    def create_module_tab(self):
        """创建模块管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # 常用模块选择
        common_group = QGroupBox("📦 常用模块选择")
        common_layout = QVBoxLayout(common_group)
        
        # 下拉框选择区域
        dropdown_layout = QHBoxLayout()
        
        self.common_modules_combo = QComboBox()
        self.common_modules_combo.setMinimumWidth(200)
        
        # 添加下拉框选项
        self.common_modules_combo.addItems([
            "📝 选择常用模块...",
            "🤖 --- 人工智能/机器学习 ---",
            "🤖 tensorflow",
            "🤖 torch", 
            "🤖 sklearn",
            "🤖 transformers",
            "🤖 opencv-python",
            "🤖 keras",
            "📈 --- 数据处理 ---",
            "📈 numpy",
            "📈 pandas",
            "📈 matplotlib",
            "📈 seaborn",
            "📈 plotly",
            "📈 scipy",
            "🖌️ --- GUI框架 ---",
            "🖌️ tkinter",
            "🖌️ PyQt5",
            "🖌️ PyQt6", 
            "🖌️ PySide2",
            "🖌️ PySide6",
            "🌍 --- 网络/API ---",
            "🌍 requests",
            "🌍 urllib3",
            "🌍 flask",
            "🌍 fastapi",
            "🔧 --- 其他常用 ---",
            "🔧 psutil",
            "🔧 sqlite3",
            "🔧 json",
            "🔧 yaml"
        ])
        
        add_common_btn = QPushButton("添加选中模块")
        add_common_btn.clicked.connect(self.add_common_module)
        
        dropdown_layout.addWidget(QLabel("选择模块:"))
        dropdown_layout.addWidget(self.common_modules_combo)
        dropdown_layout.addWidget(add_common_btn)
        dropdown_layout.addStretch()
        
        common_layout.addLayout(dropdown_layout)
        
        # 隐藏导入
        hidden_group = QGroupBox("📝 手动输入模块")
        hidden_layout = QVBoxLayout(hidden_group)
        
        hidden_controls = QHBoxLayout()
        self.hidden_edit = QLineEdit()
        self.hidden_edit.setPlaceholderText("输入模块名称，如: numpy, pandas")
        # 启用拖拽（文本拖拽）
        self.hidden_edit.setAcceptDrops(True)
        self.hidden_edit.dragEnterEvent = self.text_drag_enter_event
        self.hidden_edit.dropEvent = self.text_drop_event
        
        add_hidden_btn = QPushButton("添加")
        add_hidden_btn.clicked.connect(self.add_hidden_import)
        
        hidden_controls.addWidget(self.hidden_edit)
        hidden_controls.addWidget(add_hidden_btn)
        
        self.hidden_list = QListWidget()
        self.hidden_list.setMaximumHeight(120)
        
        remove_hidden_btn = QPushButton("删除选中")
        remove_hidden_btn.clicked.connect(self.remove_hidden_import)
        
        hidden_layout.addLayout(hidden_controls)
        hidden_layout.addWidget(self.hidden_list)
        hidden_layout.addWidget(remove_hidden_btn)
        
        # 收集模块
        collect_group = QGroupBox("📁 收集子模块")
        collect_layout = QVBoxLayout(collect_group)
        
        self.collect_edit = QLineEdit()
        self.collect_edit.setPlaceholderText("收集所有子模块，如: PIL")
        # 启用拖拽（文本拖拽）
        self.collect_edit.setAcceptDrops(True)
        self.collect_edit.dragEnterEvent = self.text_drag_enter_event
        self.collect_edit.dropEvent = self.text_drop_event
        
        collect_layout.addWidget(self.collect_edit)
        
        # 排除模块
        exclude_group = QGroupBox("❌ 排除模块")
        exclude_layout = QVBoxLayout(exclude_group)
        
        exclude_controls = QHBoxLayout()
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText("输入要排除的模块名称")
        # 启用拖拽（文本拖拽）
        self.exclude_edit.setAcceptDrops(True)
        self.exclude_edit.dragEnterEvent = self.text_drag_enter_event
        self.exclude_edit.dropEvent = self.text_drop_event
        
        add_exclude_btn = QPushButton("添加")
        add_exclude_btn.clicked.connect(self.add_exclude_module)
        
        exclude_controls.addWidget(self.exclude_edit)
        exclude_controls.addWidget(add_exclude_btn)
        
        self.exclude_list = QListWidget()
        self.exclude_list.setMaximumHeight(100)
        
        remove_exclude_btn = QPushButton("删除选中")
        remove_exclude_btn.clicked.connect(self.remove_exclude_module)
        
        exclude_layout.addLayout(exclude_controls)
        exclude_layout.addWidget(self.exclude_list)
        exclude_layout.addWidget(remove_exclude_btn)
        
        # 添加到布局
        layout.addWidget(common_group)
        layout.addWidget(hidden_group)
        layout.addWidget(collect_group)
        layout.addWidget(exclude_group)
        layout.addStretch()
        
        return widget
    
    def create_resource_tab(self):
        """创建资源文件标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # 数据文件区域
        data_group = QGroupBox("📄 数据文件")
        data_layout = QVBoxLayout(data_group)
        
        # 按钮区域
        data_controls = QHBoxLayout()
        add_data_btn = QPushButton("添加文件")
        add_data_btn.clicked.connect(self.add_data_file)
        add_data_dir_btn = QPushButton("添加目录")
        add_data_dir_btn.clicked.connect(self.add_data_directory)
        remove_data_btn = QPushButton("删除选中")
        remove_data_btn.clicked.connect(self.remove_data_file)
        
        data_controls.addWidget(add_data_btn)
        data_controls.addWidget(add_data_dir_btn)
        data_controls.addWidget(remove_data_btn)
        data_controls.addStretch()
        
        self.data_list = QListWidget()
        self.data_list.setMaximumHeight(150)
        
        data_layout.addLayout(data_controls)
        data_layout.addWidget(self.data_list)
        
        # 添加拖放区域
        data_drop_label = QLabel("📁 拖放文件或目录到此处添加数据文件")
        data_drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        data_drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #0d6efd;
                border-radius: 8px;
                padding: 15px;
                background-color: #f8f9ff;
                color: #6c757d;
                font-style: italic;
            }
        """)
        data_drop_label.setAcceptDrops(True)
        data_drop_label.dragEnterEvent = self.resource_drag_enter_event
        data_drop_label.dropEvent = self.data_drop_event
        data_layout.addWidget(data_drop_label)
        
        # 二进制文件区域
        binary_group = QGroupBox("⚙️ 二进制文件")
        binary_layout = QVBoxLayout(binary_group)
        
        # 按钮区域
        binary_controls = QHBoxLayout()
        add_binary_btn = QPushButton("添加文件")
        add_binary_btn.clicked.connect(self.add_binary_file)
        add_binary_dir_btn = QPushButton("添加目录")
        add_binary_dir_btn.clicked.connect(self.add_binary_directory)
        remove_binary_btn = QPushButton("删除选中")
        remove_binary_btn.clicked.connect(self.remove_binary_file)
        
        binary_controls.addWidget(add_binary_btn)
        binary_controls.addWidget(add_binary_dir_btn)
        binary_controls.addWidget(remove_binary_btn)
        binary_controls.addStretch()
        
        self.binary_list = QListWidget()
        self.binary_list.setMaximumHeight(150)
        
        binary_layout.addLayout(binary_controls)
        binary_layout.addWidget(self.binary_list)
        
        # 添加拖放区域
        binary_drop_label = QLabel("📁 拖放文件或目录到此处添加二进制文件")
        binary_drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        binary_drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #0d6efd;
                border-radius: 8px;
                padding: 15px;
                background-color: #f8f9ff;
                color: #6c757d;
                font-style: italic;
            }
        """)
        binary_drop_label.setAcceptDrops(True)
        binary_drop_label.dragEnterEvent = self.resource_drag_enter_event
        binary_drop_label.dropEvent = self.binary_drop_event
        binary_layout.addWidget(binary_drop_label)
        
        layout.addWidget(data_group)
        layout.addWidget(binary_group)
        layout.addStretch()
        
        return widget
    
    def create_advanced_tab(self):
        """创建高级设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # 调试选项
        debug_group = QGroupBox("🐛 调试与优化")
        debug_layout = QVBoxLayout(debug_group)
        
        self.debug_check = QCheckBox("启用调试模式 (--debug)")
        self.noupx_check = QCheckBox("禁用UPX压缩 (--noupx)")
        
        # 添加减小体积的选项
        self.strip_check = QCheckBox("移除符号表 (--strip) [Linux/macOS]")
        self.strip_check.setToolTip("移除可执行文件中的符号表，减小文件大小")
        
        self.upx_exclude_edit = QLineEdit()
        self.upx_exclude_edit.setPlaceholderText("排除模块，如: numpy,scipy")
        upx_exclude_layout = QHBoxLayout()
        upx_exclude_layout.addWidget(QLabel("UPX排除模块:"))
        upx_exclude_layout.addWidget(self.upx_exclude_edit)
        
        debug_layout.addWidget(self.debug_check)
        debug_layout.addWidget(self.noupx_check)
        debug_layout.addWidget(self.strip_check)
        debug_layout.addLayout(upx_exclude_layout)
        
        # 日志级别
        log_widget = QWidget()
        log_layout = QHBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        
        log_layout.addWidget(QLabel("日志级别:"))
        self.log_combo = QComboBox()
        self.log_combo.addItems(["DEBUG", "INFO", "WARN", "ERROR"])
        self.log_combo.setCurrentText("INFO")
        log_layout.addWidget(self.log_combo)
        log_layout.addStretch()
        
        debug_layout.addWidget(log_widget)
        
        # 优化选项
        optimization_group = QGroupBox("🔧 优化选项")
        optimization_layout = QVBoxLayout(optimization_group)
        
        self.strip_check = QCheckBox("移除符号表 (--strip) [Linux/macOS]")
        self.strip_check.setToolTip("移除可执行文件中的符号表，减小文件大小")
        
        optimization_layout.addWidget(self.strip_check)
        
        # UPX排除模块
        upx_exclude_layout = QHBoxLayout()
        upx_exclude_layout.addWidget(QLabel("UPX排除模块:"))
        self.upx_exclude_edit = QLineEdit()
        self.upx_exclude_edit.setPlaceholderText("排除模块，如: numpy,scipy")
        self.upx_exclude_edit.setToolTip("指定不使用UPX压缩的模块，用逗号分隔")
        upx_exclude_layout.addWidget(self.upx_exclude_edit)
        
        optimization_layout.addLayout(upx_exclude_layout)
        
        # 其他选项
        other_group = QGroupBox("🔐 其他选项")
        other_layout = QFormLayout(other_group)
        
        # 加密密钥
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("加密密钥（可选）")
        # 启用拖拽（文本拖拽）
        self.key_edit.setAcceptDrops(True)
        self.key_edit.dragEnterEvent = self.text_drag_enter_event
        self.key_edit.dropEvent = self.text_drop_event
        
        # 启动画面
        splash_widget = QWidget()
        splash_layout = QHBoxLayout(splash_widget)
        splash_layout.setContentsMargins(0, 0, 0, 0)
        
        self.splash_edit = QLineEdit()
        self.splash_edit.setPlaceholderText("选择启动画面图片")
        # 启用拖拽
        self.splash_edit.setAcceptDrops(True)
        self.splash_edit.dragEnterEvent = lambda event: self.generic_drag_enter_event(event, ['png', 'jpg', 'jpeg', 'bmp'])
        self.splash_edit.dropEvent = self.splash_drop_event
        splash_browse_btn = QPushButton("浏览")
        splash_browse_btn.clicked.connect(self.browse_splash)
        
        splash_layout.addWidget(self.splash_edit)
        splash_layout.addWidget(splash_browse_btn)
        
        other_layout.addRow("加密密钥:", self.key_edit)
        other_layout.addRow("启动画面:", splash_widget)
        
        layout.addWidget(debug_group)
        layout.addWidget(other_group)
        layout.addStretch()
        
        return widget
    
    def create_command_panel(self):
        """创建命令面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("🚀 生成PyInstaller命令")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
            padding: 10px;
            background-color: #e8f4fd;
            border-radius: 8px;
        """)
        
        # 命令显示区域
        self.command_text = QTextEdit()
        self.command_text.setPlaceholderText("生成的PyInstaller命令将显示在这里...\n\n点击'生成命令'后，您可以：\n1. 复制命令到剪贴板\n2. 在终端中手动执行")
        self.command_text.setMinimumHeight(250)
        
        # 按钮区域
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        generate_btn = QPushButton("🔨 生成命令")
        generate_btn.clicked.connect(self.generate_command)
        
        copy_btn = QPushButton("📋 复制命令")
        copy_btn.clicked.connect(self.copy_command)
        
        clear_btn = QPushButton("🗑️ 清空设置")
        clear_btn.clicked.connect(self.clear_all)
        
        button_layout.addWidget(generate_btn)
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addWidget(title_label)
        layout.addWidget(self.command_text)
        layout.addLayout(button_layout)
        
        return widget
    
    def apply_styles(self):
        """应用简洁现代化样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            /* 美化标签页样式 */
            QTabWidget {
                background-color: transparent;
            }
            
            QTabWidget::pane {
                border: 2px solid #e9ecef;
                border-radius: 12px;
                background-color: white;
                margin-top: 10px;
            }
            
            QTabBar {
                background-color: transparent;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                color: #6c757d;
                border: 2px solid #e9ecef;
                padding: 12px 20px;
                margin-right: 4px;
                margin-bottom: -2px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                min-width: 120px;
                font-size: 13px;
                font-weight: 500;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f8ff);
                color: #0d6efd;
                border-bottom-color: white;
                font-weight: bold;
                border-color: #0d6efd;
                border-bottom: 2px solid white;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f8ff);
                color: #495057;
                border-color: #ced4da;
            }
            
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #e3f2fd;
                border-radius: 12px;
                margin: 12px 0;
                padding-top: 16px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #fafbfc);
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 4px 12px;
                color: #1976d2;
                background-color: white;
                border: 2px solid #1976d2;
                border-radius: 8px;
                font-size: 13px;
            }
            
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 13px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border-color: #0d6efd;
                background-color: #f8f9ff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
            }
            
            QLineEdit:hover {
                border-color: #ced4da;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d6efd, stop:1 #0b5ed7);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0b5ed7, stop:1 #0a58ca);
                transform: translateY(-1px);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a58ca, stop:1 #084298);
                transform: translateY(0px);
            }
            
            QRadioButton, QCheckBox {
                font-size: 13px;
                spacing: 10px;
                padding: 6px;
                color: #495057;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            
            QRadioButton::indicator:unchecked {
                border: 2px solid #ced4da;
                border-radius: 9px;
                background-color: white;
            }
            
            QRadioButton::indicator:checked {
                border: 3px solid #0d6efd;
                border-radius: 9px;
                background-color: #0d6efd;
                width: 12px;
                height: 12px;
            }
            
            QRadioButton::indicator:checked:hover {
                border-color: #0b5ed7;
                background-color: #0b5ed7;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 2px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                border: 2px solid #0d6efd;
                border-radius: 4px;
                background-color: #0d6efd;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            
            QCheckBox::indicator:checked:hover {
                border-color: #0b5ed7;
                background-color: #0b5ed7;
            }
            
            QListWidget {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                font-size: 12px;
                padding: 6px;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
                border-radius: 4px;
                margin: 1px;
            }
            
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                color: #1976d2;
                border: 1px solid #1976d2;
            }
            
            QListWidget::item:hover {
                background-color: #f0f8ff;
            }
            
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-width: 140px;
            }
            
            QComboBox:hover {
                border-color: #ced4da;
            }
            
            QComboBox:focus {
                border-color: #0d6efd;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d6efd, stop:1 #0b5ed7);
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 2px;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid #0d6efd;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #e3f2fd;
                font-size: 12px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                margin: 1px;
                border-radius: 4px;
            }
            
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: bold;
            }
            
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
                line-height: 1.4;
            }
            
            QTextEdit:focus {
                border-color: #0d6efd;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #ced4da;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }
        """)
    
    def set_application_icon(self):
        """设置应用程序图标，优先使用项目根目录的icon.ico"""
        # 获取项目根目录（当前工作目录）
        current_dir = os.getcwd()
        icon_path = os.path.join(current_dir, "icon.ico")
        
        # 如果当前目录没有icon.ico，尝试使用icon1.ico
        if not os.path.exists(icon_path):
            icon1_path = os.path.join(current_dir, "icon1.ico")
            if os.path.exists(icon1_path):
                # 将icon1.ico复制为icon.ico用于窗口显示
                import shutil
                try:
                    shutil.copy2(icon1_path, icon_path)
                    print(f"已将 icon1.ico 复制为 icon.ico 用于窗口显示")
                except Exception as e:
                    print(f"复制图标文件失败: {e}")
                    icon_path = icon1_path  # 直接使用icon1.ico
        
        # 如果还是没有，尝试脚本所在目录
        if not os.path.exists(icon_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.ico")
            
            if not os.path.exists(icon_path):
                script_icon1_path = os.path.join(script_dir, "icon1.ico")
                if os.path.exists(script_icon1_path):
                    icon_path = script_icon1_path
        
        # 如果找到了图标文件，就使用它
        if os.path.exists(icon_path):
            try:
                icon = QIcon(icon_path)
                if not icon.isNull():
                    self.setWindowIcon(icon)
                    print(f"成功加载应用图标: {icon_path}")
                    return True
            except Exception as e:
                print(f"加载图标失败: {icon_path}, 错误: {e}")
        
        # 如果没有找到任何图标，创建一个默认图标
        print("未找到任何图标文件，使用默认图标")
        self.create_default_icon()
        return False
    
    def create_default_icon(self):
        """创建默认图标"""
        try:
            from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
            
            # 创建一个 32x32 的默认图标
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(13, 110, 253))  # 蓝色背景
            
            painter = QPainter(pixmap)
            painter.setPen(QColor(255, 255, 255))  # 白色文字
            painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "P")
            painter.end()
            
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            
        except Exception as e:
            print(f"创建默认图标失败: {e}")
    
    def center_window(self):
        """窗口居中"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    # 文件浏览方法
    def browse_script(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Python脚本文件", "", "Python文件 (*.py);;所有文件 (*.*)"
        )
        if file_path:
            self.script_edit.setText(file_path)
    
    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图标文件", "", 
            "图片文件 (*.ico *.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*.*)"
        )
        if file_path:
            self.process_icon_file(file_path)
            
    def apply_new_icon(self, icon_path):
        """应用新图标到应用程序窗口"""
        try:
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                if not icon.isNull():
                    # 设置窗口图标
                    self.setWindowIcon(icon)
                    print(f"已更新应用图标: {icon_path}")
                else:
                    print(f"图标文件无效: {icon_path}")
            else:
                print(f"图标文件不存在: {icon_path}")
        except Exception as e:
            print(f"应用图标失败: {e}")
    
    def browse_output(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder_path:
            self.output_edit.setText(folder_path)
    
    def browse_work(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择工作目录")
        if folder_path:
            self.work_edit.setText(folder_path)
    
    def browse_splash(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择启动画面图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*.*)"
        )
        if file_path:
            self.splash_edit.setText(file_path)
    
    def add_search_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择搜索路径")
        if folder_path and folder_path not in self.search_paths:
            self.search_paths.append(folder_path)
            self.search_list.addItem(folder_path)
    
    def remove_search_path(self):
        current_row = self.search_list.currentRow()
        if current_row >= 0:
            self.search_list.takeItem(current_row)
            del self.search_paths[current_row]
    
    # 拖拽事件处理
    def generic_drag_enter_event(self, event: QDragEnterEvent, allowed_extensions=None):
        """通用的拖拽进入事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:  # 只允许拖拽一个文件
                file_path = urls[0].toLocalFile()
                if allowed_extensions:
                    # 检查文件扩展名
                    file_ext = file_path.lower().split('.')[-1]
                    if file_ext in allowed_extensions:
                        event.acceptProposedAction()
                        return
                else:
                    # 没有扩展名限制，接受所有文件
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def folder_drag_enter_event(self, event: QDragEnterEvent):
        """文件夹拖拽进入事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                path = urls[0].toLocalFile()
                if os.path.isdir(path):  # 只接受文件夹
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def text_drag_enter_event(self, event: QDragEnterEvent):
        """文本拖拽进入事件处理"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def folder_drop_event(self, event: QDropEvent, target_edit):
        """文件夹拖拽放置事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                path = urls[0].toLocalFile()
                if os.path.isdir(path):
                    target_edit.setText(path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def resource_drag_enter_event(self, event: QDragEnterEvent):
        """资源文件拖拽进入事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:  # 只允许拖拽一个文件或目录
                path = urls[0].toLocalFile()
                # 接受文件或目录
                if os.path.exists(path):
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def data_drop_event(self, event: QDropEvent):
        """数据文件拖拽放置事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                path = urls[0].toLocalFile()
                if os.path.exists(path):
                    # 自动判断是文件还是目录
                    if os.path.isfile(path):
                        self.add_data_file_by_path(path)
                    elif os.path.isdir(path):
                        self.add_data_directory_by_path(path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def binary_drop_event(self, event: QDropEvent):
        """二进制文件拖拽放置事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                path = urls[0].toLocalFile()
                if os.path.exists(path):
                    # 自动判断是文件还是目录
                    if os.path.isfile(path):
                        self.add_binary_file_by_path(path)
                    elif os.path.isdir(path):
                        self.add_binary_directory_by_path(path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def text_drop_event(self, event: QDropEvent):
        """文本拖拽放置事件处理"""
        if event.mimeData().hasText():
            text = event.mimeData().text().strip()
            # 获取当前触发事件的控件
            source = event.source() if hasattr(event, 'source') else None
            if not source:
                # 如果无法获取source，使用sender
                source = self.sender()
            
            # 确保source是QLineEdit类型
            if source and isinstance(source, QLineEdit):
                source.setText(text)
                event.acceptProposedAction()
                return
        event.ignore()
    
    def icon_drop_event(self, event: QDropEvent):
        """图标文件拖拽放置事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                allowed_extensions = ['ico', 'png', 'jpg', 'jpeg', 'bmp', 'gif']
                file_ext = file_path.lower().split('.')[-1]
                if file_ext in allowed_extensions:
                    # 使用现有的图标处理逻辑
                    self.process_icon_file(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def splash_drop_event(self, event: QDropEvent):
        """启动画面图片拖拽放置事件处理"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                allowed_extensions = ['png', 'jpg', 'jpeg', 'bmp']
                file_ext = file_path.lower().split('.')[-1]
                if file_ext in allowed_extensions:
                    self.splash_edit.setText(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def process_icon_file(self, file_path):
        """处理图标文件（从拖拽或浏览中选择）"""
        # 获取项目根目录（脚本所在目录）
        project_root = os.path.dirname(os.path.abspath(self.script_edit.text())) if self.script_edit.text().strip() else os.getcwd()
        
        # 统一使用 icon.ico 作为最终文件名（用于窗口显示）
        final_icon_path = os.path.join(project_root, 'icon.ico')
        
        # 检查是否选择的就是当前根目录下的 icon.ico 文件
        if os.path.abspath(file_path) == os.path.abspath(final_icon_path):
            # 直接使用现有的 icon.ico 文件
            self.icon_edit.setText(file_path)
            # 立即应用图标到应用程序窗口
            self.apply_new_icon(file_path)
            QMessageBox.information(self, "信息", "已选择项目根目录下的 icon.ico 文件")
            return
        
        # 检查是否选择的是 icon1.ico（用于任务栏显示）
        icon1_path = os.path.join(project_root, 'icon1.ico')
        if os.path.abspath(file_path) == os.path.abspath(icon1_path):
            # 将 icon1.ico 复制为 icon.ico 用于窗口显示
            import shutil
            try:
                if os.path.exists(final_icon_path):
                    os.remove(final_icon_path)
                shutil.copy2(file_path, final_icon_path)
                self.icon_edit.setText(final_icon_path)
                self.apply_new_icon(final_icon_path)
                QMessageBox.information(self, "信息", "已使用 icon1.ico 作为程序图标，同时复制为 icon.ico 用于窗口显示")
                return
            except Exception as e:
                QMessageBox.warning(self, "警告", f"无法处理图标文件: {str(e)}")
                return
        
        # 先删除已存在的 icon.ico 文件（只有在选择其他文件时才删除）
        if os.path.exists(final_icon_path):
            try:
                os.remove(final_icon_path)
                print(f"已删除旧的图标文件: {final_icon_path}")
            except Exception as e:
                QMessageBox.warning(self, "警告", f"无法删除旧的图标文件: {str(e)}")
                return
        
        # 如果不是ico格式，自动转换
        if not file_path.lower().endswith('.ico'):
            ico_path = self.convert_to_ico(file_path, project_root)
            if ico_path:
                file_path = ico_path
            else:
                return  # 转换失败，终止处理
        else:
            # 如果是ico文件，复制并重命名为icon.ico
            if file_path != final_icon_path:
                import shutil
                try:
                    shutil.copy2(file_path, final_icon_path)
                    file_path = final_icon_path
                    QMessageBox.information(self, "信息", "图标文件已复制到项目根目录并重命名为: icon.ico")
                except Exception as e:
                    QMessageBox.warning(self, "警告", f"无法复制图标文件: {str(e)}")
                    return
        
        self.icon_edit.setText(file_path)
        
        # 立即应用新图标到应用程序窗口
        self.apply_new_icon(file_path)
    def script_drag_enter_event(self, event: QDragEnterEvent):
        """处理脚本文件拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:  # 只允许拖拽一个文件
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith('.py'):  # 只接受Python文件
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def script_drop_event(self, event: QDropEvent):
        """处理脚本文件拖拽放置事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith('.py'):
                    self.script_edit.setText(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def convert_to_ico(self, image_path, output_dir=None):
        """将图片转换为ico格式并保存到指定目录，统一命名为icon.ico"""
        try:
            # 确定输出目录
            if output_dir is None:
                output_dir = os.path.dirname(image_path)
            
            # 统一使用 icon.ico 作为文件名
            ico_path = os.path.join(output_dir, 'icon.ico')
            
            # 注意：这里不需要删除旧文件，因为在browse_icon中已经处理了
            
            # 使用PIL转换
            with Image.open(image_path) as img:
                # 转换为RGBA模式并调整尺寸
                img = img.convert('RGBA')
                # ico文件常用尺寸
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(ico_path, format='ICO', sizes=sizes)
            
            QMessageBox.information(self, "成功", f"图片已转换为 ico 格式：icon.ico")
            return ico_path
        except Exception as e:
            QMessageBox.warning(self, "警告", f"图片转换失败：{str(e)}")
            # 转换失败，返回None表示失败
            return None
    
    def add_common_module(self):
        """添加下拉框选中的常用模块"""
        selected_text = self.common_modules_combo.currentText()
        
        # 过滤掉提示文本和分组标题
        if (
            selected_text.endswith("选择常用模块...") or 
            "---" in selected_text
        ):
            return
        
        # 移除图标，获取模块名
        module = selected_text.split(" ", 1)[-1].strip()
        
        if module and module not in self.hidden_imports:
            self.hidden_imports.append(module)
            
            # 根据模块类型显示不同图标
            icon = "📦"  # 默认图标
            if any(ai_module in module.lower() for ai_module in ['tensorflow', 'torch', 'sklearn', 'keras']):
                icon = "🤖"  # AI模块
            elif any(data_module in module.lower() for data_module in ['numpy', 'pandas', 'matplotlib', 'scipy']):
                icon = "📈"  # 数据处理
            elif any(gui_module in module.lower() for gui_module in ['qt', 'tk', 'kivy', 'pyside']):
                icon = "🖌️"  # GUI
            elif any(net_module in module.lower() for net_module in ['request', 'urllib', 'flask', 'fastapi']):
                icon = "🌍"  # 网络
            
            self.hidden_list.addItem(f"{icon} {module}")
            
            # 重置下拉框到默认选项
            self.common_modules_combo.setCurrentIndex(0)
    
    def add_exclude_module(self):
        module = self.exclude_edit.text().strip()
        if module and module not in self.exclude_modules:
            self.exclude_modules.append(module)
            self.exclude_list.addItem(f"❌ {module}")
            self.exclude_edit.clear()
    
    def remove_exclude_module(self):
        current_row = self.exclude_list.currentRow()
        if current_row >= 0:
            self.exclude_list.takeItem(current_row)
            del self.exclude_modules[current_row]
    
    def add_binary_file(self):
        """添加单个二进制文件"""
        # 确定起始目录
        start_dir = ""
        if self.first_binary_dialog and self.script_edit.text().strip():
            # 首次打开且有脚本文件时，定位到脚本所在目录
            start_dir = os.path.dirname(os.path.abspath(self.script_edit.text()))
            self.first_binary_dialog = False  # 标记已不是首次
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择二进制文件", start_dir, 
            "二进制文件 (*.dll *.so *.dylib *.exe);;所有文件 (*.*)"
        )
        if file_path:
            self.add_binary_file_by_path(file_path)
    
    def add_binary_file_by_path(self, file_path):
        """通过路径添加二进制文件"""
        file_name = os.path.basename(file_path)
        
        # 提供更合理的默认目标路径
        default_target = "."
        
        target_path, ok = QInputDialog.getText(
            self, "设置目标路径", 
            f"源文件: {file_path}\n\n请设置在可执行文件中的目标路径:\n\n示例:\n• '.' - 放在根目录下\n• 'lib' - 放在lib文件夹下\n• 'bin/{file_name}' - 指定具体文件名和路径", 
            text=default_target
        )
        
        if ok and target_path.strip():
            entry = f"{file_path};{target_path.strip()}"
            if entry not in self.binary_files:
                self.binary_files.append(entry)
                display_text = f"⚙️ {file_path} → {target_path.strip()}"
                self.binary_list.addItem(display_text)
    
    def add_binary_directory(self):
        """添加二进制目录"""
        # 确定起始目录
        start_dir = ""
        if self.first_binary_dialog and self.script_edit.text().strip():
            # 首次打开且有脚本文件时，定位到脚本所在目录
            start_dir = os.path.dirname(os.path.abspath(self.script_edit.text()))
            self.first_binary_dialog = False  # 标记已不是首次
        
        folder_path = QFileDialog.getExistingDirectory(self, "选择二进制目录", start_dir)
        if folder_path:
            self.add_binary_directory_by_path(folder_path)
    
    def add_binary_directory_by_path(self, folder_path):
        """通过路径添加二进制目录"""
        folder_name = os.path.basename(folder_path)
        
        # 提供更合理的默认目标路径 - 目录情况下默认使用目录名称
        default_target = folder_name
        
        target_path, ok = QInputDialog.getText(
            self, "设置目标路径", 
            f"源目录: {folder_path}\n\n请设置在可执行文件中的目标路径:\n\n示例:\n• '.' - 将目录内容直接放在根目录下\n• '{folder_name}' - 保持原目录名\n• 'lib' - 重命名为lib目录", 
            text=default_target
        )
        
        if ok and target_path.strip():
            entry = f"{folder_path};{target_path.strip()}"
            if entry not in self.binary_files:
                self.binary_files.append(entry)
                display_text = f"📁 {folder_path} → {target_path.strip()}"
                self.binary_list.addItem(display_text)
    
    def remove_binary_file(self):
        current_row = self.binary_list.currentRow()
        if current_row >= 0:
            self.binary_list.takeItem(current_row)
            del self.binary_files[current_row]
    
    # 模块管理方法
    def add_hidden_import(self):
        module = self.hidden_edit.text().strip()
        if module and module not in self.hidden_imports:
            self.hidden_imports.append(module)
            self.hidden_list.addItem(f"📦 {module}")
            self.hidden_edit.clear()
    
    def remove_hidden_import(self):
        current_row = self.hidden_list.currentRow()
        if current_row >= 0:
            self.hidden_list.takeItem(current_row)
            del self.hidden_imports[current_row]
    
    # 资源文件管理方法
    def add_data_file(self):
        """添加单个数据文件"""
        # 确定起始目录
        start_dir = ""
        if self.first_data_dialog and self.script_edit.text().strip():
            # 首次打开且有脚本文件时，定位到脚本所在目录
            start_dir = os.path.dirname(os.path.abspath(self.script_edit.text()))
            self.first_data_dialog = False  # 标记已不是首次
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", start_dir, "所有文件 (*.*)"
        )
        if file_path:
            self.add_data_file_by_path(file_path)
    
    def add_data_file_by_path(self, file_path):
        """通过路径添加数据文件"""
        file_name = os.path.basename(file_path)
        
        # 提供更合理的默认目标路径
        default_target = "."
        
        target_path, ok = QInputDialog.getText(
            self, "设置目标路径", 
            f"源文件: {file_path}\n\n请设置在可执行文件中的目标路径:\n\n示例:\n• '.' - 放在根目录下\n• 'data' - 放在data文件夹下\n• 'config/settings.ini' - 指定具体文件名和路径", 
            text=default_target
        )
        
        if ok and target_path.strip():
            entry = f"{file_path};{target_path.strip()}"
            if entry not in self.data_files:
                self.data_files.append(entry)
                display_text = f"📄 {file_path} → {target_path.strip()}"
                self.data_list.addItem(display_text)
    
    def add_data_directory(self):
        """添加数据目录"""
        # 确定起始目录
        start_dir = ""
        if self.first_data_dialog and self.script_edit.text().strip():
            # 首次打开且有脚本文件时，定位到脚本所在目录
            start_dir = os.path.dirname(os.path.abspath(self.script_edit.text()))
            self.first_data_dialog = False  # 标记已不是首次
        
        folder_path = QFileDialog.getExistingDirectory(self, "选择数据目录", start_dir)
        if folder_path:
            self.add_data_directory_by_path(folder_path)
    
    def add_data_directory_by_path(self, folder_path):
        """通过路径添加数据目录"""
        folder_name = os.path.basename(folder_path)
        
        # 提供更合理的默认目标路径 - 目录情况下默认使用目录名称
        default_target = folder_name
        
        target_path, ok = QInputDialog.getText(
            self, "设置目标路径", 
            f"源目录: {folder_path}\n\n请设置在可执行文件中的目标路径:\n\n示例:\n• '.' - 将目录内容直接放在根目录下\n• '{folder_name}' - 保持原目录名\n• 'data' - 重命名为data目录", 
            text=default_target
        )
        
        if ok and target_path.strip():
            entry = f"{folder_path};{target_path.strip()}"
            if entry not in self.data_files:
                self.data_files.append(entry)
                display_text = f"📁 {folder_path} → {target_path.strip()}"
                self.data_list.addItem(display_text)
    
    def remove_data_file(self):
        current_row = self.data_list.currentRow()
        if current_row >= 0:
            self.data_list.takeItem(current_row)
            del self.data_files[current_row]
    
    # 命令生成和操作
    def generate_command(self):
        """生成PyInstaller命令"""
        if not self.script_edit.text().strip():
            QMessageBox.warning(self, "警告", "请选择Python脚本文件！")
            return
        
        command_parts = ["pyinstaller"]
        
        # 基本模式
        if self.onefile_radio.isChecked():
            command_parts.append("-F")
        else:
            command_parts.append("-D")
        
        # 窗口模式
        if self.windowed_radio.isChecked():
            command_parts.append("-w")
        else:
            command_parts.append("-c")
        
        # 图标
        if self.icon_edit.text().strip():
            icon_path = self.icon_edit.text()
            # 确保图标文件存在
            if os.path.exists(icon_path):
                # 获取项目根目录
                project_root = os.path.dirname(os.path.abspath(self.script_edit.text())) if self.script_edit.text().strip() else os.getcwd()
                
                # 检查是否存在 icon1.ico（优先使用作为任务栏图标）
                icon1_path = os.path.join(project_root, 'icon1.ico')
                if os.path.exists(icon1_path):
                    # 使用 icon1.ico 作为任务栏图标
                    icon_path = os.path.abspath(icon1_path)
                    command_parts.append(f'-i "{icon_path}"')
                    print(f"使用 icon1.ico 作为任务栏图标: {icon_path}")
                else:
                    # 使用用户选择的图标文件
                    icon_path = os.path.abspath(icon_path)
                    command_parts.append(f'-i "{icon_path}"')
                    print(f"使用用户选择的图标: {icon_path}")
            else:
                # 如果文件不存在，给出警告但不添加图标参数
                print(f"警告：图标文件不存在: {icon_path}")
        
        # 程序名称
        if self.name_edit.text().strip():
            command_parts.append(f'-n "{self.name_edit.text()}"')
        
        # 路径选项
        if self.output_edit.text().strip():
            command_parts.append(f'--distpath "{self.output_edit.text()}"')
        
        if self.work_edit.text().strip():
            command_parts.append(f'--workpath "{self.work_edit.text()}"')
        
        # 搜索路径
        for path in self.search_paths:
            command_parts.append(f'-p "{path}"')
        
        # 数据文件
        for data_file in self.data_files:
            command_parts.append(f'--add-data "{data_file}"')
        
        # 二进制文件
        for binary_file in self.binary_files:
            command_parts.append(f'--add-binary "{binary_file}"')
        
        # 隐藏导入
        for module in self.hidden_imports:
            command_parts.append(f'--hidden-import {module}')
        
        # 收集模块
        if self.collect_edit.text().strip():
            command_parts.append(f'--collect-submodules {self.collect_edit.text()}')
        
        # 排除模块
        for module in self.exclude_modules:
            command_parts.append(f'--exclude-module {module}')
        
        # 调试选项
        if self.debug_check.isChecked():
            command_parts.append("--debug")
        
        if self.clean_check.isChecked():
            command_parts.append("--clean")
        
        if self.noupx_check.isChecked():
            command_parts.append("--noupx")
        
        if self.noconfirm_check.isChecked():
            command_parts.append("-y")
        
        if self.log_combo.currentText() != "INFO":
            command_parts.append(f'--log-level {self.log_combo.currentText()}')
        
        # 其他选项
        if self.uac_check.isChecked():
            command_parts.append("--uac-admin")
        
        # 优化选项
        if self.strip_check.isChecked():
            command_parts.append("--strip")
        
        # UPX排除模块
        upx_exclude_text = self.upx_exclude_edit.text().strip()
        if upx_exclude_text:
            modules = [m.strip() for m in upx_exclude_text.split(",") if m.strip()]
            for module in modules:
                command_parts.append(f'--upx-exclude "{module}"')
        
        if self.key_edit.text().strip():
            command_parts.append(f'--key "{self.key_edit.text()}"')
        
        if self.splash_edit.text().strip():
            command_parts.append(f'--splash "{self.splash_edit.text()}"')
        
        # 添加脚本文件
        command_parts.append(f'"{self.script_edit.text()}"')
        
        # 生成最终命令
        command = " ".join(command_parts)
        self.command_text.setPlainText(command)
    
    def copy_command(self):
        """复制命令到剪贴板"""
        command = self.command_text.toPlainText().strip()
        if command:
            QApplication.clipboard().setText(command)
            QMessageBox.information(self, "成功", "命令已复制到剪贴板！")
        else:
            QMessageBox.warning(self, "警告", "请先生成命令！")
    
    def clear_all(self):
        """清空所有设置"""
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 清空所有控件
            self.script_edit.clear()
            self.onedir_radio.setChecked(True)
            self.console_radio.setChecked(True)
            self.icon_edit.clear()
            self.name_edit.clear()
            self.output_edit.clear()
            self.work_edit.clear()
            self.collect_edit.clear()
            self.key_edit.clear()
            self.splash_edit.clear()
            
            # 清空复选框
            self.debug_check.setChecked(False)
            self.clean_check.setChecked(False)
            self.noupx_check.setChecked(False)
            self.noconfirm_check.setChecked(True)  # 重新设置为默认状态
            self.uac_check.setChecked(False)
            
            # 重置组合框
            self.log_combo.setCurrentText("INFO")
            
            # 清空列表
            self.search_paths.clear()
            self.data_files.clear()
            self.binary_files.clear()
            self.hidden_imports.clear()
            self.exclude_modules.clear()
            
            # 清空优化选项
            self.strip_check.setChecked(False)
            self.upx_exclude_edit.clear()
            
            # 清空列表控件
            self.search_list.clear()
            self.data_list.clear()
            self.binary_list.clear()
            self.hidden_list.clear()
            self.exclude_list.clear()
            
            # 清空命令文本
            self.command_text.clear()
            
            # 重置常用模块下拉框
            if hasattr(self, 'common_modules_combo'):
                self.common_modules_combo.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyInstaller GUI")
    app.setApplicationVersion("3.0 - Simple")
    app.setApplicationDisplayName("PyInstaller 命令构建器")
    app.setOrganizationName("PyInstaller GUI Tool")
    
    # 优先设置应用程序图标（在窗口创建前）
    # 查找当前目录的icon.ico
    current_dir = os.getcwd()
    icon_path = os.path.join(current_dir, "icon.ico")
    
    # 如果当前目录没有，尝试脚本所在目录
    if not os.path.exists(icon_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icon.ico")
    
    if os.path.exists(icon_path):
        try:
            app.setWindowIcon(QIcon(icon_path))
            print(f"应用程序图标设置成功: {icon_path}")
        except Exception as e:
            print(f"设置应用图标失败: {e}")
    else:
        print("未找到icon.ico文件")
    
    window = PyInstallerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()