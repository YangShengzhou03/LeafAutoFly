# LeafAuto PRO（枫叶信息自动化专业版）

> 🌟 让重复办公任务更轻松，用 AI 助手 + 自动化脚本提升微信效率的桌面工具

[![License: GPL-2.0](https://img.shields.io/badge/License-GPL--2.0-blue.svg)](./LICENSE)
![GitHub stars](https://img.shields.io/github/stars/Yangshengzhou/lucky-smss?style=social)
---

## 📚 目录

1. [项目简介](#项目简介)
2. [技术栈与依赖说明](#技术栈与依赖说明)
3. [目录结构详解](#目录结构详解)
4. [环境搭建与部署指南](#环境搭建与部署指南)
5. [开发者指南：如何进行二次开发？](#开发者指南如何进行二次开发)
6. [模块功能解析与使用方法](#模块功能解析与使用方法)
7. [常见问题 FAQ](#常见问题-faq)
8. [扩展建议与插件系统规划](#扩展建议与插件系统规划)
9. [联系方式与贡献方式](#联系方式与贡献方式)
10. [许可协议](#许可协议)

---

## 🌟 项目简介

**LeafAuto PRO** 是一款基于 PyQt6 和 Python 的本地桌面自动化工具，专注于帮助用户简化日常重复性办公任务、调用 AI 助手、管理活动流程，并通过多线程技术保障界面流畅和系统稳定。

### 💡 项目初衷

在日常工作场景中，很多操作都是高度重复且机械化的，比如：
- 复制粘贴数据
- 模拟点击按钮
- 批量处理文件
- 调用 API 获取数据
- 定时执行任务

虽然这些任务可以通过编写脚本来完成，但对普通用户来说门槛太高。而市面上一些 RPA 工具又过于复杂或昂贵。

因此，我们设计了 **LeafAuto PRO**，一个轻量级、可视化、可扩展、适合新手和开发者的桌面自动化工具。

LeafAuto PRO 专业版在任务执行效率与多任务兼容性方面进行了深度优化。相较于普通版本，其在处理微信信息发送任务时拥有更快的响应速度，并支持与前台用户操作无缝并行运行，确保在执行自动化任务期间不影响正常的桌面交互体验。

---

## ⚙️ 技术栈与依赖说明

LeafAuto PRO 基于现代 Python 生态构建，采用模块化架构，确保良好的可维护性和可拓展性。

| 类别       | 技术/库                  | 版本     | 用途说明                             |
|------------|--------------------------|----------|--------------------------------------|
| 编程语言   | Python                   | 3.11+    | 主程序语言                           |
| GUI框架    | PyQt6                    | 6.4.2    | 构建图形界面                         |
| UI设计     | Qt Designer              | -        | 可视化拖拽布局                       |
| 打包工具   | PyInstaller              | 5.6.2    | 打包成 Windows/Linux/macOS 可执行文件 |
| HTTP请求   | requests                 | 2.32.3   | 用于调用外部 API（如AI助手）         |
| 多线程     | QThread / Thread.py      | -        | 并发处理后台任务                     |
| 进程控制   | QSharedMemory / pywin32  | 308      | 单实例限制，Windows平台支持          |
| 第三方库   | wxauto                   | 3.9.11+  | 微信自动化相关功能                   |

---

## 🗂️ 目录结构详解

以下是当前项目的完整文件结构（基于你提供的 GitHub 结构），并附上每个文件的作用说明：

```
.
├── Application.py                        # 主程序入口点
├── common.py                             # 公共函数、日志、配置读取等
├── LeafAuto_version_info.txt             # 版本信息文件（用于打包时嵌入版本号）
├── LeafAuto封装脚本.iss                  # Inno Setup 安装包脚本（Windows）
├── LeafProcess.py                        # 进程控制类（用于跨进程通信）
├── LICENSE.md                            # MIT 许可证文件
├── MainWindow.py                         # 主窗口逻辑处理代码
├── README.md                             # 当前文档
├── Reply.py                              # 回复模块（可能用于对话框/提示弹窗）
├── SettingWindow.py                      # 设置窗口逻辑
├── Split.py                              # 文件分割模块
├── System_info.py                        # 获取系统信息（CPU、内存、磁盘等）
├── Thread.py                             # 多线程任务基类
├── UpdateDialog.py                       # 更新检测与下载模块
├── Ui_MainWindow.py                      # 自动生成的主窗口UI类
├── Ui_Activities.py                      # 活动窗口UI类
├── Ui_SettingWindow.py                   # 设置窗口UI类
├── resources/                            # 图标、图片等资源文件夹
│   └── logo.ico                          # 应用图标
├── QT_Ui/                                # Qt Designer 原始 .ui 文件
│   ├── Ui_MainWindow.ui
│   ├── Ui_Activities.ui
│   ├── Ui_SettingWindow.ui
│   └── ...
└── requirements.txt                      # 依赖库清单
```

### 文件详细说明

#### Application.py —— 主程序入口

这是整个程序的启动器，负责初始化 QApplication、加载主窗口、设置全局变量、注册事件监听器等。

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

#### common.py —— 公共函数、日志、配置读取等

包含了一些公共函数，例如日志记录、配置文件读取等功能。

```python
import logging

def setup_logging():
    logger = logging.getLogger('leafauto')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
```

#### LeafAuto_version_info.txt —— 版本信息文件

存储应用版本号，方便打包时嵌入。

```
Version: 1.0.0
Release Date: 2025-05-06
```

#### LeafAuto封装脚本.iss —— Inno Setup 安装包脚本（Windows）

用于生成 Windows 安装包的脚本文件。

```ini
[Setup]
AppName=LeafAuto PRO
AppVersion=1.0.0
DefaultDirName={pf}\LeafAuto PRO
OutputBaseFilename=LeafAuto_PRO_setup
Compression=lzma
SolidCompression=yes
```

#### LeafProcess.py —— 进程控制类

实现跨进程通信的功能。

```python
from multiprocessing import Process, Queue

def worker(queue):
    queue.put("Hello from worker!")
```

#### MainWindow.py —— 主窗口逻辑

该模块包含主窗口的所有交互逻辑，包括菜单栏、按钮响应、窗口切换等。

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LeafAuto PRO')
        self.setGeometry(300, 300, 800, 600)
```

#### SettingWindow.py —— 设置窗口逻辑

设置窗口的逻辑处理。

```python
class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 400, 300)
```

#### System_info.py —— 系统信息获取

获取系统的硬件信息，如 CPU 使用率、内存使用情况等。

```python
import psutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {"cpu": cpu_usage, "memory": memory_info.percent}
```

#### Thread.py —— 多线程任务管理

避免阻塞主线程，所有耗时操作都应放到子线程中执行。

```python
from PyQt6.QtCore import QThread, pyqtSignal

class Worker(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.progress.emit(i)
```
### 🛠️ 环境搭建与部署指南

为了确保所有用户都能顺利运行 LeafAuto PRO，无论是开发者还是最终用户，我们提供了详细的环境搭建和部署指南。

#### ✅ 一、安装依赖环境

首先需要确保你的系统已经安装了 Python 3.11 或更高版本。推荐使用虚拟环境来管理项目的依赖项，以避免与其他项目发生冲突。

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装依赖库
pip install -r requirements.txt
```

如果你在安装过程中遇到任何问题，请检查 `requirements.txt` 文件是否正确，并确保你的网络连接正常。

#### ✅ 二、运行项目

完成依赖安装后，你可以通过以下命令启动 LeafAuto PRO：

```bash
python Application.py
```

这将启动主应用程序窗口，你可以开始使用 LeafAuto PRO 的各种功能。

#### ✅ 三、打包为可执行文件（Windows）

对于想要发布或分发 LeafAuto PRO 的用户，可以使用 PyInstaller 将 Python 脚本打包成独立的可执行文件。

```bash
pyinstaller --onefile --windowed Application.spec
```

生成的 `.exe` 文件将在 `dist/` 目录下。你可以直接双击运行这个文件，无需再安装 Python 或其他依赖。

##### 使用 Inno Setup 打包成安装包

如果你想进一步创建一个安装包，以便用户可以通过简单的双击进行安装，可以使用 Inno Setup 工具。以下是基本步骤：

1. 下载并安装 [Inno Setup](http://www.jrsoftware.org/isinfo.php)。
2. 修改 `LeafAuto封装脚本.iss` 文件中的路径、图标、版本号等信息。
3. 打开 `LeafAuto封装脚本.iss` 文件，点击“编译”按钮，生成 `.exe` 安装包。

---

## 🧑‍💻 开发者指南：如何进行二次开发？

对于希望对 LeafAuto PRO 进行二次开发的用户，这里提供了一些指导和建议。

### 🧱 1. 新增一个功能模块（例如：新建一个“定时任务”功能）

#### 步骤如下：
1. **设计UI界面**：在 Qt Designer 中打开 `QT_Ui/MainWindow.ui` 文件，添加一个新的菜单项或按钮。
   
   ![Qt Designer Screenshot](path/to/screenshot.png)

2. **创建新的UI类**：如果需要，可以在 `QT_Ui/` 文件夹下创建一个新的 `.ui` 文件（比如 `Ui_TaskScheduler.ui`），然后用 `pyuic6` 命令将其转换为 Python 类文件。

   ```bash
   pyuic6 QT_Ui/Ui_TaskScheduler.ui -o Ui_TaskScheduler.py
   ```

3. **实现业务逻辑**：创建 `TaskScheduler.py` 文件，继承自 `QWidget` 或 `QDialog`，并在其中加载 UI 类。

   ```python
   from PyQt6.QtWidgets import QWidget
   from .Ui_TaskScheduler import Ui_TaskScheduler

   class TaskScheduler(QWidget, Ui_TaskScheduler):
       def __init__(self):
           super().__init__()
           self.setupUi(self)
           # 绑定事件
           self.startButton.clicked.connect(self.start_task)
       
       def start_task(self):
           # 实现定时任务逻辑
           pass
   ```

4. **集成到主程序中**：在 `Application.py` 或 `MainWindow.py` 中导入新模块，并绑定相应的事件处理函数。

   ```python
   from TaskScheduler import TaskScheduler

   class MainWindow(QMainWindow):
       def __init__(self):
           super().__init__()
           self.task_scheduler = TaskScheduler()
           self.menuBar().addAction("Task Scheduler", self.show_task_scheduler)
       
       def show_task_scheduler(self):
           self.task_scheduler.show()
   ```

5. **后台任务支持**：如果需要长时间运行的任务，可以考虑使用多线程技术。参考 `Thread.py` 中的 `Worker` 类实现。

### 🔧 2. 修改现有界面（例如：调整主窗口布局）

1. **修改UI文件**：打开 `QT_Ui/MainWindow.ui` 使用 Qt Designer 进行界面布局调整。

2. **重新生成UI类文件**：保存后重新生成 `Ui_MainWindow.py` 文件。

   ```bash
   pyuic6 QT_Ui/MainWindow.ui -o Ui_MainWindow.py
   ```

3. **更新逻辑代码**：根据新的UI布局，在 `MainWindow.py` 中更新对应的逻辑代码。

### 📦 3. 打包发布

除了前面提到的 PyInstaller 和 Inno Setup 方法外，你还可以使用其他工具如 cx_Freeze 来打包你的应用。选择最适合你需求的方式即可。

---

## 🧪 模块功能解析与使用方法

### 📌 Application.py —— 主程序入口

这是整个程序的启动器，负责初始化 QApplication、加载主窗口、设置全局变量、注册事件监听器等。

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

### 📌 MainWindow.py —— 主窗口逻辑

该模块包含主窗口的所有交互逻辑，包括菜单栏、按钮响应、窗口切换等。

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LeafAuto PRO')
        self.setGeometry(300, 300, 800, 600)
```

### 📌 AiAssistant.py —— AI 助手模块

调用 OpenAI 或其他 AI API，实现自然语言处理、智能问答、脚本生成等功能。

```python
import requests

def query_ai_assistant(user_input):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}]
        }
    )
    return response.json()
```

### 📌 Thread.py —— 多线程任务管理

为了避免界面卡顿，所有耗时操作都应放到子线程中执行。

```python
from PyQt6.QtCore import QThread, pyqtSignal

class MyWorker(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.progress.emit(i)
```

### 📌 System_info.py —— 获取系统信息

获取系统的硬件信息，如 CPU 使用率、内存使用情况等。

```python
import psutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {"cpu": cpu_usage, "memory": memory_info.percent}
```

---

## ❓ 常见问题 FAQ

### Q1：运行时报错找不到某个模块怎么办？
A：请确认是否执行了 `pip install -r requirements.txt`，特别是 `wxauto` 需要手动安装 wheel 包。

### Q2：为什么不能同时运行多个实例？
A：项目使用 `QSharedMemory` 实现单实例机制，防止误启动多个程序造成冲突。

### Q3：怎么自定义主题颜色？
A：可在 `common.py` 中找到 `load_stylesheet()` 方法，替换为自己的 CSS 样式即可。

### Q4：如何查看日志？
A：默认会输出日志到终端，也可以修改 `common.py` 将日志写入文件。

### Q5：我想自己添加一个插件系统，怎么做？
A：建议创建一个 `plugins/` 目录，采用动态导入方式加载模块。你可以参考 `AutoInfo.py` 的设计思路。

---

## 🧩 扩展建议与插件系统规划

我们计划在未来引入插件系统，允许用户或第三方开发者扩展功能模块。

### 插件系统初步规划：

- **插件格式**：`.zip` 或 `.plugin` 文件，内含 Python 模块和元数据。
- **加载方式**：运行时动态导入。
- **权限控制**：沙箱机制，限制访问权限。
- **插件商店**：未来将上线官方插件市场。

---

## 🤝 联系方式与贡献方式

欢迎任何形式的贡献！无论是提交 Bug、优化代码、完善文档还是提出新功能建议，都欢迎您参与进来！

- 🐱 GitHub 仓库：[Yangshengzhou/LeafAutoPRO](https://github.com/Yangshengzhou/LeafAutoPRO)
- 📝 博客文章（持续更新）：[https://blog.csdn.net/Yang_shengzhou/article/details/143782041]
- 📧 联系邮箱：yangsz03@foxmail.com

---

## 📜 许可协议

该项目采用 [MIT License](LICENSE.md)，您可以自由使用、修改和分发，但需保留原版权声明及许可声明。

---

## ❤️ 最后一句话

> “如果你也厌倦了每天定时发微信，那就来试试 LeafAuto PRO 吧，让工作变得高效而有趣。”

---