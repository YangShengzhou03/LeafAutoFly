<div align="center">
  <h1>🌟 LeafAuto PRO 开发文档</h1>
</div>


<div align="center">
  <a href="https://github.com/YangShengzhou03/LeafAutoPRO">
    <img src="https://img.shields.io/github/stars/YangShengzhou03/LeafAutoPRO?style=for-the-badge&logo=github" alt="GitHub Stars">
  </a>
  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="MIT License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11.4-blue?style=for-the-badge&logo=python" alt="Python Version">
  </a>
</div>


> 🌟 让重复办公任务更轻松，用 AI 助手 + 自动化脚本提升微信效率的桌面工具


## 📚 目录

1. [项目简介](#项目简介)
2. [技术栈与依赖说明](#技术栈与依赖说明)
3. [目录结构详解](#目录结构详解)
4. [环境搭建与部署指南](#环境搭建与部署指南)
5. [开发者指南：如何进行二次开发？](#开发者指南如何进行二次开发)
6. [模块功能解析与使用方法](#模块功能解析与使用方法)
7. [常见问题 FAQ](#常见问题-faq)
8. [扩展建议与插件系统规划](#扩展建议与插件系统规划)
9. [社区与支持](#社区与支持)
10. [许可证（MIT）](#许可证mit)
11. [未来规划](#未来规划)
12. [结语](#结语)
13. [联系与支持](#联系与支持)

---

## 🌟 项目简介

**LeafAuto PRO** 是一款基于 PyQt6 和 Python 的本地桌面自动化工具，专注于帮助用户简化日常重复性办公任务、调用 AI 助手、管理活动流程，并通过多线程技术保障界面流畅和系统稳定。

### 💡 项目初衷

在日常工作场景中，很多操作都是高度重复且机械化的，比如：
- 定时定点发送信息
- 群资料机器人
- 批量处理文件
- 调用 API 获取数据
- 自动回复群成员信息

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

以下是当前项目的完整文件结构，并附上每个文件的作用说明：

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

- **Application.py**：程序启动入口，负责初始化应用、加载主窗口及全局配置
- **common.py**：封装公共功能，包括日志记录、配置读取、通用工具函数等
- **MainWindow.py**：主窗口逻辑处理，包含界面交互、菜单响应、模块调用等核心功能
- **SettingWindow.py**：设置窗口逻辑，管理用户偏好配置、参数调整等功能
- **System_info.py**：获取系统硬件信息（CPU、内存、磁盘等），用于性能监控
- **Thread.py**：多线程任务管理基类，确保耗时操作不阻塞界面响应
- **UpdateDialog.py**：版本更新检测与下载模块，支持自动升级功能

---

## 🛠️ 环境搭建与部署指南

为了确保所有用户都能顺利运行 LeafAuto PRO，无论是开发者还是最终用户，我们提供了详细的环境搭建和部署指南。

### ✅ 一、安装依赖环境

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

### ✅ 二、运行项目

完成依赖安装后，你可以通过以下命令启动 LeafAuto PRO：

```bash
python Application.py
```

这将启动主应用程序窗口，你可以开始使用 LeafAuto PRO 的各种功能。

### ✅ 三、打包为可执行文件（Windows）

对于想要发布或分发 LeafAuto PRO 的用户，可以使用 PyInstaller 将 Python 脚本打包成独立的可执行文件。

```bash
pyinstaller Application.spec
```

生成的 `.exe` 文件将在 `dist/` 目录下。你可以直接双击运行这个文件，无需再安装 Python 或其他依赖。

#### 使用 Inno Setup 打包成安装包

如果你想进一步创建一个安装包，以便用户可以通过简单的双击进行安装，可以使用 Inno Setup 工具。以下是基本步骤：

1. 下载并安装 [Inno Setup](http://www.jrsoftware.org/isinfo.php)。
2. 修改 `LeafAuto封装脚本.iss` 文件中的路径、图标、版本号等信息。
3. 打开 `LeafAuto封装脚本.iss` 文件，点击“编译”按钮，生成 `.exe` 安装包。

---

## 🧑‍💻 开发者指南：如何进行二次开发？

对于希望对 LeafAuto PRO 进行二次开发的用户，这里提供了一些指导和建议。

### 🧱 1. 新增一个功能模块（例如：新建一个“定时任务”功能）

#### 步骤如下：
1. **设计UI界面**：在 Qt Designer 中打开 `QT_Ui/MainWindow.ui` 文件，添加新的菜单项或按钮。
2. **创建新的UI类**：如需独立窗口，在 `QT_Ui/` 文件夹下创建新的 `.ui` 文件（如 `Ui_TaskScheduler.ui`），并通过 `pyuic6` 命令转换为Python类文件。
3. **实现业务逻辑**：创建对应逻辑文件（如 `TaskScheduler.py`），继承UI类并实现功能逻辑。
4. **集成到主程序**：在主窗口代码中导入新模块，绑定菜单或按钮事件，实现功能调用。
5. **后台任务支持**：对于耗时操作，使用多线程技术避免界面卡顿，可参考 `Thread.py` 中的实现方式。

### 🔧 2. 修改现有界面（例如：调整主窗口布局）

1. **修改UI文件**：使用 Qt Designer 打开对应 `.ui` 文件进行布局调整。
2. **重新生成UI类**：通过 `pyuic6` 命令将修改后的 `.ui` 文件转换为Python类文件。
3. **更新逻辑代码**：根据新的界面布局，调整对应逻辑文件中的交互处理代码。

### 📦 3. 打包发布

除了前面提到的 PyInstaller 和 Inno Setup 方法外，也可使用 cx_Freeze 等工具打包应用，选择最适合需求的方式即可。

---

## 🧪 模块功能解析与使用方法

### 📌 核心模块说明

- **主程序入口（Application.py）**：负责初始化应用、加载配置、启动主窗口，是程序的启动点。
  
- **主窗口模块（MainWindow.py）**：包含所有界面交互逻辑，如菜单操作、按钮响应、窗口切换等，是用户操作的主要入口。

- **AI助手模块**：集成人工智能能力，支持自然语言交互、智能问答、自动化脚本生成等功能，提升用户操作效率。

- **多线程任务管理（Thread.py）**：采用多线程机制处理耗时任务，确保在执行自动化操作时界面保持流畅响应，不影响用户正常使用。

- **系统信息模块（System_info.py）**：实时监测系统资源使用情况，包括CPU使用率、内存占用等，为性能优化提供数据支持。

---

## ❓ 常见问题 FAQ

### Q1：运行时报错找不到某个模块怎么办？
A：请确认是否执行了 `pip install -r requirements.txt`，特别是 `wxauto` 需要手动安装wheel包。

### Q2：为什么不能同时运行多个实例？
A：项目使用单实例机制，防止误启动多个程序造成冲突，保障操作稳定性。

### Q3：怎么自定义主题颜色？
A：可在 `common.py` 关联的样式文件中修改CSS样式，实现主题颜色自定义。

### Q4：如何查看日志？
A：默认会输出日志到终端，也可通过配置将日志写入文件，便于问题排查。

### Q5：想添加插件系统，怎么做？
A：建议创建 `plugins/` 目录，采用动态导入方式加载模块，可参考现有模块的设计思路。

---

## 🧩 扩展建议与插件系统规划

我们计划在未来引入插件系统，允许用户或第三方开发者扩展功能模块。

### 插件系统初步规划：

- **插件格式**：`.zip` 或 `.plugin` 文件，内含Python模块和元数据。
- **加载方式**：运行时动态导入，支持热插拔。
- **权限控制**：沙箱机制，限制插件访问范围，保障系统安全。
- **插件商店**：未来将上线官方插件市场，提供丰富的扩展资源。

---

## 🤝 社区与支持

如果你在使用过程中遇到问题，或者有任何改进建议，欢迎参与讨论：

- 🐞 GitHub Issues: [https://github.com/YangShengzhou03/LeafAutoPRO/issues](https://github.com/YangShengzhou03/LeafAutoPRO/issues)  
- 💬 Gitee 项目地址: [https://gitee.com/Yangshengzhou/LeafAutoPRO](https://gitee.com/Yangshengzhou/LeafAutoPRO)  
- 👨‍💻 作者主页: [https://github.com/YangShengzhou03](https://github.com/YangShengzhou03)  

---

## 📜 许可证（MIT）

该项目采用 [MIT 开源协议](https://opensource.org/licenses/MIT) 发布。

这意味着你可以：

- ✅ 自由使用、复制、修改和分发该软件  
- ✅ 将软件用于商业用途  

但必须遵守以下规则：

- 🚫 不得去除版权声明和许可条款  
- 🚫 若修改源代码并重新分发，需在衍生作品中保留原作者版权信息  
- 🚫 不得以任何形式声称这是你的原创作品而不注明来源  

详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🚀 未来规划

虽然当前版本已具备核心自动化功能，但我们仍在持续优化和扩展，未来计划包括：

- 🎛️ 可视化流程设计器：无需代码即可通过拖拽创建自动化流程  
- 📊 任务执行报表：生成详细的自动化任务统计与分析报告  
- 🔄 智能调度中心：支持任务优先级设置和定时执行策略  
- 🌍 多语言界面：支持中英文等多语言切换，适配不同用户需求  
- 📱 移动控制端：通过手机APP远程监控和控制自动化任务  
- 🧩 开放API接口：允许其他应用程序调用LeafAuto的自动化能力  

---

## 💬 结语

大家好，我是 Yangshengzhou，`LeafAuto` 的开发者。

`LeafAuto`源于一个听起来有点离谱的起点：**为了在 2024 年 5 月 20 日 0 点准时向女友发送浪漫小作文，却由于困倦熬不住夜**。于是写下了 `LeafAuto` 的第一行代码，最初的终端版本就这样诞生了。

没想到，这个 “偷懒” 的小工具意外得到了很多朋友的喜欢。加上当时我正在学桌面软件开发，便慢慢打磨出了带图形界面的版本。

后来才发现，有太多人和我有过类似的困扰：为了定时工作、报岗不得不熬夜，被重复的微信消息搞得疲惫不堪，试过不少工具却要么不好用，要么价格不菲。于是我下定决心，把 `LeafAuto` 做得更完善，让它能真正解决这些 “重复劳动” 的痛点。

如今，LeafAuto PRO 被寄予厚望，希望它能帮你从机械重复的事务中抽离出来，把时间留给更值得的人和事情。
> “让自动化成为效率的翅膀，而非技术的门槛。”

如果你觉得这个项目对你有帮助，请别忘了给个 ⭐ star 和 🍴 fork，这是对我最大的鼓励！

祝你的工作越来越顺利，天天开心 ✨

---

## 📞 联系与支持  

- **项目主页**：[https://gitee.com/Yangshengzhou/LeafAutoPRO](https://gitee.com/Yangshengzhou/LeafAutoPRO)  
- **文档中心**：[https://yangshengzhou.gitbook.io/leafautopro](https://yangshengzhou.gitbook.io/leafautopro)  
- **问题反馈**：[提交Issue](https://gitee.com/Yangshengzhou/LeafAutoPRO/issues)  
- **商务合作**：yangsz03@foxmail.com（主题注明"`LeafAuto PRO`合作"）  
- **社区交流**：  
[![微信](https://img.shields.io/badge/微信-YSZFortune-brightgreen?logo=wechat)](https://img.shields.io/badge/微信-YSZFortune-brightgreen?logo=wechat) [![QQ群](https://img.shields.io/badge/QQ群-1021471813-blue?logo=tencentqq)](https://img.shields.io/badge/QQ群-1021471813-blue?logo=tencentqq)

---

© 2025 Yangshengzhou. All rights reserved.  
Powered by MIT License.