# LeafAuto·Web 🚀 | 智能网页自动化平台

<div align="center">
  <a href="https://www.gnu.org/licenses/agpl-3.0">
    <img src="https://img.shields.io/badge/License-AGPL_v3-blue?style=for-the-badge&logo=gnu" alt="License: AGPL v3">
  </a>
  <a href="https://github.com/YangShengzhou03/LeafAutoWeb">
    <img src="https://img.shields.io/github/stars/YangShengzhou03/LeafAutoWeb?style=for-the-badge&logo=github" alt="GitHub Stars">
  </a>
  <a href="https://github.com/YangShengzhou03/LeafAutoWeb">
    <img src="https://img.shields.io/github/forks/YangShengzhou03/LeafAutoWeb?style=for-the-badge&logo=github" alt="GitHub Forks">
  </a>
</div>

📦 **有限开源协议** | ⚙️ **自动化工作流引擎** | 🤖 **AI增强能力**

---

## 📌 目录

1. [简介](#简介)
2. [核心功能](#核心功能)
3. [支持场景](#支持场景)
4. [安装部署](#安装部署)
5. [快速上手](#快速上手)
6. [技术架构](#技术架构)
7. [实现原理](#实现原理)
8. [核心优势](#核心优势)
9. [社区与支持](#社区与支持)
10. [许可证（AGPL-3.0）](#许可证agpl-30)
11. [开发路线图](#开发路线图)
12. [贡献指南](#贡献指南)
13. [结语](#结语)

---

## 简介

LeafAuto·Web 是一款**AI驱动的网页自动化平台**，旨在通过可视化界面帮助用户构建、执行和管理自动化工作流。无论是重复性数据处理、定时任务执行，还是复杂业务流程的自动化，都能通过简单配置实现，让用户从机械劳动中解放出来，专注于创造性工作。

平台融合了**智能调度系统**、**自然语言处理**和**多端通知**能力，提供从任务创建到结果反馈的全流程自动化支持，适用于个人效率提升与团队协作场景。

## 核心功能

### 🔄 任务自动化引擎
- 可视化任务编辑器，支持拖拽式流程设计
- 定时/触发式任务调度，精确到秒级执行控制
- 任务依赖管理与批量执行
- 执行日志实时追踪与异常重试机制

### 🤖 AI增强模块
- 自然语言转自动化指令（支持中文/英文）
- 智能错误修复与流程优化建议
- 基于历史数据的任务执行预测
- 上下文感知的对话式操作助手

### 📱 多端协同能力
- 微信消息实时通知（任务状态/执行结果）
- 跨设备任务同步与远程控制
- 权限分级的团队协作管理
- 数据导出与第三方系统集成（API）

### 🎨 交互体验优化
- 自适应布局，支持桌面/平板多终端访问
- 深色/浅色模式一键切换
- 可定制的仪表盘与快捷操作
- 操作引导与功能提示系统

## 支持场景

- **日常办公自动化**：报表生成、邮件批量处理、文档格式转换
- **数据管理**：网页数据抓取、Excel批量处理、数据库定时备份
- **监控告警**：网站可用性检测、服务器状态监控、异常情况通知
- **内容运营**：社交媒体定时发布、内容聚合与整理
- **开发辅助**：日志分析、代码格式化、测试用例自动生成

## 安装部署

### 环境要求
- Python 3.8+
- 1GB以上内存
- 支持Windows/macOS/Linux系统

### 快速安装步骤

1. **克隆仓库到本地**
   ```bash
   git clone https://github.com/YangShengzhou03/LeafAutoWeb.git
   cd LeafAutoWeb
   ```

2. **创建并激活虚拟环境（推荐）**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

4. **初始化配置文件**
   ```bash
   cp config.example.py config.py
   # 根据需求编辑config.py设置端口/数据库等参数
   ```

5. **启动应用**
   ```bash
   # 开发模式
   python application.py --debug
   
   # 生产模式
   python application.py --production
   ```

6. **访问系统**  
   打开浏览器访问 `http://localhost:5000`（默认端口），首次登录使用默认账号：`admin`，密码：`leafauto123`（建议登录后立即修改）

## 快速上手

### 入门指南：创建第一个自动化任务

1. 登录系统后，在左侧导航栏点击「任务管理」→「新建任务」
2. 在任务编辑器中：
   - 输入任务名称（如"每日数据备份"）
   - 选择触发方式（定时触发/手动触发）
   - 配置执行步骤（可拖拽预设组件）
   - 设置通知方式（微信/系统消息）
3. 点击「测试执行」验证任务正确性
4. 确认无误后点击「保存并启用」，任务将按设定规则自动执行

### 核心页面导航

- **仪表盘**：查看任务执行统计、快捷操作入口
- **任务中心**：管理所有自动化任务（创建/编辑/删除/启用）
- **AI助手**：通过自然语言生成自动化流程
- **日志中心**：查询历史执行记录与错误详情
- **系统设置**：配置用户偏好、权限管理、集成服务

## 技术架构

### 项目结构

```
LeafAuto_Web/
│
├── application.py        # Flask主应用
├── config.py             # 配置设置
├── scheduler.py          # 任务调度入口
├── requirements.txt      # 依赖列表
├── models.py             # 数据库模型
├── utils.py              # 工具函数
├── extensions.py         # Flask扩展
├── README.md             # 项目说明文件
│
├── static/               # 静态资源
│   ├── css/
│   │   ├── main.css      # 主样式表
│   │   ├── element.css   # UI库样式覆盖
│   │   └── dark.css      # 深色模式样式
│   │
│   └── js/
│       ├── lib/          # 第三方库
│       │   ├── vue.global.js
│       │   └── element-plus.js
│       │
│       └── modules/      # 功能模块
│           ├── scheduler.js
│           ├── ai.js
│           └── settings.js
│
├── templates/            # Jinja2模板
│   ├── index.html        # 首页
│   │
│   ├── layouts/          # 基础布局
│   │   ├── base.html
│   │   └── admin.html
│   │
│   ├── components/       # 可复用组件
│   │   ├── ai_console.html
│   │   ├── task_form.html
│   │   └── time_picker.html
│   │
│   └── pages/            # 功能页面
│       ├── scheduler.html
│       ├── ai.html
│       └── settings.html
│
└── modules/              # Python模块
    ├── core/             # 核心功能
    │   ├── __init__.py
    │   ├── scheduler.py  # 调度逻辑
    │   └── wechat.py     # 微信集成
    │
    └── ai/               # AI功能
        ├── __init__.py
        ├── nlp.py        # NLP处理
        └── dialog.py     # 对话管理
```

### 技术栈说明
- **后端**：Flask框架 + SQLite/MySQL数据库
- **前端**：Vue 3 + Element Plus组件库
- **任务调度**：基于APScheduler实现定时任务
- **AI能力**：集成Transformer模型实现自然语言处理
- **通信层**：WebSocket实时反馈执行状态

## 实现原理

LeafAuto·Web采用**分层架构设计**，核心工作流程如下：

1. **任务定义层**：用户通过可视化界面定义自动化流程，系统将其转换为可执行的JSON格式配置
2. **调度引擎层**：基于时间规则或事件触发，将任务加入执行队列
3. **执行引擎层**：解析任务配置，按步骤执行对应操作，实时记录执行状态
4. **反馈层**：将执行结果通过预设渠道（微信/系统内）通知用户

AI增强功能通过**自然语言转流程**模块实现：用户输入文字描述（如"每天晚上8点下载XX网站的数据并发送到邮箱"），系统通过NLP解析意图，自动生成对应的任务配置，简化复杂流程的创建难度。

## 核心优势

- **低代码门槛**：无需编程基础，通过可视化界面完成自动化配置
- **高度可扩展**：支持自定义组件开发，轻松集成企业内部系统
- **轻量化部署**：单文件部署模式，无需复杂的服务器配置
- **数据安全**：本地部署模式确保敏感数据不泄露，支持数据加密存储
- **持续进化**：活跃的开发迭代，定期更新功能与修复问题

## 社区与支持

### 获取帮助

- **官方文档**：访问 [项目Wiki](https://github.com/YangShengzhou03/LeafAutoWeb/wiki) 获取详细教程
- **问题反馈**：在GitHub [Issues](https://github.com/YangShengzhou03/LeafAutoWeb/issues) 提交bug报告或功能建议
- **讨论交流**：加入项目 [Discussions](https://github.com/YangShengzhou03/LeafAutoWeb/discussions) 参与社区讨论
- **QQ交流群**：123456789（验证信息：LeafAuto用户）

### 常见问题

- **Q：任务执行失败如何排查？**  
  A：在「日志中心」查看详细错误信息，或点击「重新执行并调试」获取实时执行过程

- **Q：是否支持多用户使用？**  
  A：支持，管理员可在「系统设置」→「用户管理」中创建不同权限的账号

- **Q：能否部署到服务器供团队使用？**  
  A：可以，修改config.py中的`host`参数为`0.0.0.0`，并配置端口映射即可

## 许可证（AGPL-3.0）

本项目采用 **GNU Affero General Public License v3.0** 许可证开源，允许：
- 自由使用、修改和分发本软件
- 用于商业用途（需遵守许可证条款）

**重要限制**：
- 任何基于本项目修改的衍生作品必须以相同许可证开源
- 若通过网络提供本软件的服务，必须向用户提供源代码访问权限

完整许可证文本参见项目根目录的 [LICENSE](LICENSE) 文件。

## 开发路线图

### 近期计划（1-3个月）
- 增加OCR图文识别功能，支持发票识别等场景
- 优化移动端适配体验
- 新增10+常用自动化模板（邮件营销/数据清洗等）

### 中期规划（3-6个月）
- 集成Docker部署支持，简化多环境配置
- 开发API网关，支持与企业ERP/CRM系统对接
- 实现任务版本控制与回滚功能

### 远期目标（6+个月）
- 推出SaaS版本，支持云端部署与多租户管理
- 开发AI流程推荐系统，基于用户习惯智能推荐自动化方案
- 构建插件市场，支持第三方开发者贡献功能组件

## 贡献指南

我们欢迎任何形式的贡献，包括但不限于：

1. **代码贡献**
   -  Fork本仓库
   -  创建特性分支（`git checkout -b feature/amazing-feature`）
   -  提交修改（`git commit -m 'Add some amazing feature'`）
   -  推送到分支（`git push origin feature/amazing-feature`）
   -  提交Pull Request

2. **文档完善**
   - 补充使用教程
   - 优化API文档
   - 翻译多语言版本

3. **反馈建议**
   - 提交Issue报告bug
   - 在Discussions提出功能建议
   - 分享使用场景与最佳实践

贡献者将被列入项目致谢名单，核心贡献者将获得项目维护权限。详细贡献规范参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 结语

LeafAuto·Web 诞生于对"自动化解放生产力"的信念，我们相信技术的价值在于让复杂的事情变简单，让重复的工作被自动化。

无论你是希望提升个人效率的职场人，还是寻求流程优化的企业团队，LeafAuto·Web 都能为你提供灵活可靠的自动化解决方案。

期待你的使用与反馈，让我们共同打造更智能的自动化平台！

---

*"自动化不是为了替代人，而是让人专注于更有价值的创造"* —— LeafAuto团队
