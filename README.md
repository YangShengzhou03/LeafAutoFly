# 🚀 LeafAuto Web - 微信消息自动化管理系统 🌟

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
  <a href="https://github.com/YangShengzhou03/LeafAutoWeb/issues">
    <img src="https://img.shields.io/github/issues/YangShengzhou03/LeafAutoWeb?style=for-the-badge&logo=github" alt="GitHub Issues">
  </a>
  <a href="https://github.com/YangShengzhou03/LeafAutoWeb/pulls">
    <img src="https://img.shields.io/github/issues-pr/YangShengzhou03/LeafAutoWeb?style=for-the-badge&logo=github" alt="GitHub Pull Requests">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Theme-%231e40af-blue?style=for-the-badge" alt="Theme Color: Klein Blue">
  </a>
  <a href="https://github.com/YangShengzhou03/LeafAutoWeb/commits/main">
    <img src="https://img.shields.io/github/last-commit/YangShengzhou03/LeafAutoWeb?style=for-the-badge&logo=github" alt="Last Commit">
  </a>
</div>

📌 **专业领域**：微信消息自动化 | 任务调度 | AI 自动回复
📦 开源项目 | ⚙️ 跨平台应用 | 📈 自动化任务管理 + AI 辅助回复

---

## 📌 目录

1. [简介](#简介)  
2. [核心功能](#核心功能)  
3. [技术栈](#技术栈)  
4. [系统架构](#系统架构)  
5. [安装指南](#安装指南)  
6. [使用教程](#使用教程)  
7. [项目结构](#项目结构)  
8. [API 文档](#api-文档)  
9. [贡献指南](#贡献指南)  
10. [许可证](#许可证)  
11. [联系方式](#联系方式)

---

## 📌 简介

**LeafAuto Web** 是一款功能强大的微信消息自动化发送和管理系统，基于 Flask 和 Vue 3 开发。系统专为需要高效管理微信消息发送的个人和企业用户设计，提供定时发送、重复发送规则设置以及 AI 辅助回复等功能。

### 解决的核心问题：
- 企业用户需要定期向客户发送通知、提醒或营销消息的效率问题
- 个人用户希望自动化生日提醒、节日问候等重复性沟通
- 客服人员需要快速响应常见问题，减轻工作负担
- 缺乏技术背景的用户也能轻松设置和管理自动化消息任务

### 核心价值：
- 📱 **微信消息自动化**：设置定时发送任务，解放双手，提高效率
- 🔄 **灵活的重复规则**：支持单次、每日、每周、每月及自定义重复模式
- 🤖 **AI 自动回复**：配置 AI 接管消息回复，支持多种回复风格，智能应对各类咨询
- 📊 **任务管理**：直观查看、编辑和删除自动化任务，状态一目了然
- 🔒 **数据安全**：本地部署，数据完全掌控在自己手中，保障信息安全
- 💼 **会员体系**：提供不同层级的会员服务，满足不同规模用户的需求
- 🎨 **现代界面设计**：采用克莱因蓝(#1e40af)作为主题色，界面美观且风格一致
- ⚡ **优化性能**：清理冗余代码，提升系统响应速度和运行效率

无论是个人用户用于日常提醒，还是企业用户用于客户维护、活动通知，LeafAuto Web 都能显著提升消息发送效率，降低人工成本，实现沟通自动化。

---

## 🚀 核心功能

系统采用前后端分离架构，所有数据交互通过 RESTful API 实现，确保数据实时同步和系统稳定性。

### 1. 消息自动化发送
- **定时发送**：设置具体的发送时间，精确到分钟，确保消息准时送达
- **重复发送**：支持单次、每日、每周、每月及自定义重复规则，满足各种场景需求
- **多接收者**：支持同时向多个接收者发送消息，支持批量操作
- **消息模板**：保存常用消息模板，快速创建任务，减少重复工作
- **字符统计**：实时显示消息字符数，避免超出限制
- **发送状态跟踪**：查看消息发送状态，失败自动重试

### 2. AI 自动回复
- **AI 接管开关**：一键启用/禁用 AI 自动回复功能
- **回复延迟设置**：设置回复延迟时间，使回复更自然，避免机械感
- **回复风格选择**：支持正式、友好、幽默、专业等多种回复风格
- **回复长度控制**：限制 AI 回复的最大长度，适应不同场景需求
- **关键词过滤**：设置优先处理的关键词，确保重要消息优先响应
- **回复模板**：自定义 AI 回复模板，支持变量替换，个性化回复
- **回复历史记录**：查看 AI 回复的历史记录，持续优化回复效果
- **上下文理解**：AI 能够理解对话上下文，提供连贯的回复

### 3. 任务管理
- **任务列表**：查看所有创建的自动化任务，支持排序和筛选
- **任务状态**：查看任务执行状态（待执行、已执行、失败）
- **任务编辑**：修改现有任务的各项参数，灵活调整
- **任务删除**：删除不需要的任务，保持任务列表整洁
- **任务搜索**：根据关键词搜索任务，快速定位所需任务
- **任务导出**：支持导出任务列表，方便数据分析和备份

### 4. 会员管理
- **会员等级**：提供免费版、月度会员、季度会员和年度会员
- **权限控制**：不同会员等级享有不同功能权限，如消息发送数量、AI 回复次数等
- **会员状态**：查看会员有效期和订阅状态
- **订阅管理**：便捷订阅和续费会员服务，支持多种支付方式

### 5. 系统监控
- **自动化能力统计**：显示自动化任务完成率、成功率等关键指标
- **AI 能力统计**：显示 AI 辅助功能使用率、满意度等数据
- **系统状态**：监控系统运行状态，及时发现并解决问题
- **更新状态**：检查软件更新，获取最新功能和安全补丁

---

## 🛠️ 技术栈

### 前端技术栈
- **框架**：Vue 3
- **UI 组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **HTTP 客户端**：Axios
- **构建工具**：Vite
- **代码规范**：ESLint, Prettier

### 后端技术栈
- **框架**：Flask
- **数据存储**：JSON 文件（可扩展至数据库如 MySQL、MongoDB）
- **任务调度**：APScheduler
- **API 设计**：RESTful API
- **认证授权**：JWT
- **日志管理**：Python logging

### 开发工具
- **版本控制**：Git
- **代码编辑器**：VS Code, PyCharm
- **容器化**：Docker
- **CI/CD**：GitHub Actions

---

## 🏗️ 系统架构

LeafAuto Web 采用前后端分离的架构设计，主要分为以下几个层次：

1. **前端层**：基于 Vue 3 和 Element Plus 构建的用户界面，负责与用户交互
2. **API 网关层**：处理前后端通信，实现请求路由、身份验证和权限控制
3. **业务逻辑层**：实现核心业务功能，如任务调度、AI 回复处理等
4. **数据访问层**：负责与数据存储系统交互
5. **基础设施层**：提供系统运行所需的基础服务，如日志、配置管理等

### 数据流设计
1. 用户在前端界面发起操作请求
2. 前端通过 Axios 发送 HTTP 请求到后端 API
3. 后端 API 接收请求，进行身份验证和权限检查
4. 业务逻辑层处理请求，进行相应的业务操作
5. 数据访问层与数据存储系统交互，获取或存储数据
6. 后端将处理结果返回给前端
7. 前端更新界面显示

---

## 📦 安装指南

### 方法一：源码安装

1. 克隆仓库
```bash
# 克隆 GitHub 仓库
git clone https://github.com/YangShengzhou03/LeafAutoWeb.git
cd LeafAutoWeb
```

2. 安装后端依赖
```bash
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
# 安装依赖
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
# 安装 Node.js 依赖
npm install
```

4. 初始化数据文件
```bash
# 创建数据目录
mkdir -p data
# 初始化任务数据文件
echo '[]' > data/tasks.json
# 初始化AI设置数据文件
echo '{"ai_takeover_enabled": false, "reply_delay": 1, "reply_style": "friendly", "max_reply_length": 200, "keywords": [], "reply_template": ""}' > data/ai_settings.json
# 初始化AI历史记录数据文件
echo '[]' > data/ai_history.json
```

5. 配置环境变量
```bash
# 创建 .env 文件
echo 'FLASK_APP=app.py' > .env
echo 'FLASK_ENV=development' >> .env
echo 'SECRET_KEY=your-secret-key' >> .env
```

### 方法二：Docker 容器安装

```bash
# 拉取 Docker 镜像
docker pull yangshengzhou/leafautoweb:latest

# 运行容器
docker run -d -p 8080:8080 \
  -v /path/to/data:/app/data \
  -e SECRET_KEY=your-secret-key \
  yangshengzhou/leafautoweb:latest
```

### 方法三：Windows 快捷启动

双击运行 `test_server.bat` 文件，自动完成环境配置和服务启动。

---

## 📖 使用教程

### 启动应用

1. 启动后端服务
```bash
# 在虚拟环境中运行
python app.py
```

2. 启动前端服务
```bash
npm run serve
```

3. 在浏览器中访问 `http://localhost:8080`

### 创建自动化消息任务

1. 点击左侧菜单栏中的「自动信息」
2. 填写接收者信息（多个接收者用逗号分隔）
3. 选择发送时间
4. 设置重复选项（可选）
5. 输入消息内容
6. 点击「创建任务」按钮

### 配置 AI 自动回复

1. 点击左侧菜单栏中的「AI 接管」
2. 打开「AI 接管状态」开关
3. 设置回复延迟时间
4. 选择回复风格
5. 设置最大回复长度
6. 输入关键词过滤（可选）
7. 填写回复模板（可选）
8. 点击「保存设置」按钮

### 查看任务统计

1. 点击左侧菜单栏中的「统计分析」
2. 查看自动化任务完成率、成功率等指标
3. 查看 AI 回复统计数据
4. 导出统计报告（可选）

---

## 📂 项目结构

```
LeafAutoWeb/
├── README.md               # 项目说明文档
├── LICENSE                 # 许可证文件
├── app.py                  # Flask 后端入口
├── requirements.txt        # 后端依赖列表
├── package.json            # 前端依赖配置
├── package-lock.json       # 前端依赖锁定文件
├── .gitignore              # Git 忽略文件
├── .env                    # 环境变量配置
├── .eslintrc.js            # ESLint 配置
├── prettier.config.js      # Prettier 配置
├── vue.config.js           # Vue 配置
├── data_manager.py         # 数据管理模块
├── server_manager.py       # 服务器管理模块
├── src/                    # 前端源代码
│   ├── App.vue             # 根组件
│   ├── main.js             # 前端入口
│   ├── router/             # 路由配置
│   │   └── index.js        # 路由定义
│   ├── views/              # 视图组件
│   │   ├── AppLayout.vue   # 应用布局
│   │   ├── HomeView.vue    # 首页
│   │   ├── AutoInfoView.vue # 自动信息页面
│   │   ├── AITakeoverView.vue # AI 接管页面
│   │   └── StatsView.vue   # 统计分析页面
│   ├── components/         # 公共组件
│   │   ├── TaskForm.vue    # 任务表单组件
│   │   ├── TaskList.vue    # 任务列表组件
│   │   └── AISettings.vue  # AI 设置组件
│   ├── assets/             # 静态资源
│   │   ├── css/            # 样式文件
│   │   └── images/         # 图片资源
│   ├── utils/              # 工具函数
│   └── api/                # API 封装
├── data/                   # 数据存储目录
│   ├── tasks.json          # 任务数据存储文件
│   ├── ai_settings.json    # AI设置数据存储文件
│   └── ai_history.json     # AI历史记录数据存储文件
├── test/                   # 测试目录
│   ├── test_api.py         # API 测试
│   └── test_data_manager.py # 数据管理测试
└── test_server.bat         # Windows 测试服务器脚本
```

---

## 📄 API 文档

### 基础信息
- **API 根路径**：`/api`
- **请求格式**：JSON
- **响应格式**：JSON
- **认证方式**：JWT Token
- **错误处理**：统一返回错误码和错误信息

### 认证 API

#### 登录
- **URL**: `/api/auth/login`
- **方法**: `POST`
- **请求体**: 
  ```json
  {
    "username": "admin",
    "password": "password123"
  }
  ```
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "登录成功",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user_info": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin"
      }
    }
  }
  ```
- **错误响应**: 
  ```json
  {
    "code": 401,
    "message": "用户名或密码错误",
    "data": null
  }
  ```

#### 注册
- **URL**: `/api/auth/register`
- **方法**: `POST`
- **请求体**: 
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
  }
  ```
- **响应**: 
  ```json
  {
    "code": 201,
    "message": "注册成功",
    "data": null
  }
  ```

#### 刷新 Token
- **URL**: `/api/auth/refresh`
- **方法**: `POST`
- **请求头**: `Authorization: Bearer <refresh_token>`
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "Token 刷新成功",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
  ```

### 任务管理 API

#### 获取所有任务
- **URL**: `/api/tasks`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **参数**: 
  - `status` (可选): 任务状态 (pending/completed/failed)
  - `page` (可选): 页码，默认 1
  - `per_page` (可选): 每页数量，默认 10
  - `sort_by` (可选): 排序字段，默认 'create_time'
  - `order` (可选): 排序顺序，'asc' 或 'desc'，默认 'desc'
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 100,
      "page": 1,
      "per_page": 10,
      "tasks": [
        {
          "id": 1,
          "recipients": ["user1@example.com", "user2@example.com"],
          "send_time": "2024-05-20T14:30:00",
          "repeat_type": "daily",
          "message_content": "您的每日提醒",
          "template_id": null,
          "status": "pending",
          "created_at": "2024-05-19T10:00:00",
          "updated_at": "2024-05-19T10:00:00"
        },
        // 更多任务...
      ]
    }
  }
  ```

#### 创建新任务
- **URL**: `/api/tasks`
- **方法**: `POST`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 
  ```json
  {
    "recipients": ["user1@example.com", "user2@example.com"],
    "send_time": "2024-05-20T14:30:00",
    "repeat_type": "daily",
    "repeat_config": {
      "interval": 1,
      "ends": "never",
      "end_date": null
    },
    "message_content": "您的每日提醒",
    "template_id": null
  }
  ```
- **响应**: 
  ```json
  {
    "code": 201,
    "message": "创建成功",
    "data": {
      "id": 1,
      "recipients": ["user1@example.com", "user2@example.com"],
      "send_time": "2024-05-20T14:30:00",
      "repeat_type": "daily",
      "message_content": "您的每日提醒",
      "status": "pending",
      "created_at": "2024-05-19T10:00:00"
    }
  }
  ```

#### 获取单个任务
- **URL**: `/api/tasks/<task_id>`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "id": 1,
      "recipients": ["user1@example.com", "user2@example.com"],
      "send_time": "2024-05-20T14:30:00",
      "repeat_type": "daily",
      "repeat_config": {
        "interval": 1,
        "ends": "never",
        "end_date": null
      },
      "message_content": "您的每日提醒",
      "template_id": null,
      "status": "pending",
      "created_at": "2024-05-19T10:00:00",
      "updated_at": "2024-05-19T10:00:00",
      "execution_history": [
        {
          "time": "2024-05-19T14:30:00",
          "status": "success",
          "details": "发送成功"
        }
      ]
    }
  }
  ```

#### 更新任务
- **URL**: `/api/tasks/<task_id>`
- **方法**: `PUT`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 任务信息（与创建任务相同）
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "recipients": ["user1@example.com"],
      "send_time": "2024-05-21T14:30:00",
      "repeat_type": "weekly",
      "message_content": "您的每周提醒",
      "status": "pending",
      "updated_at": "2024-05-19T11:00:00"
    }
  }
  ```

#### 删除任务
- **URL**: `/api/tasks/<task_id>`
- **方法**: `DELETE`
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "删除成功",
    "data": null
  }
  ```

#### 更新任务状态
- **URL**: `/api/tasks/<task_id>/status`
- **方法**: `PATCH`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 
  ```json
  {
    "status": "completed"
  }
  ```
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "id": 1,
      "status": "completed",
      "updated_at": "2024-05-20T14:35:00"
    }
  }
  ```

### AI 设置 API

#### 获取 AI 设置
- **URL**: `/api/ai-settings`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "ai_takeover_enabled": true,
      "reply_delay": 2,
      "min_reply_interval": 60,
      "reply_style": "professional",
      "max_reply_length": 300,
      "contact_person": "文件传输助手",
      "ai_persona": "你是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。",
      "keywords": ["紧急", "重要"],
      "custom_rules": [],
      "reply_template": "您好，{{username}}，关于您的问题，{{response}}"
    }
  }
  ```

#### 更新 AI 设置
- **URL**: `/api/ai-settings`
- **方法**: `POST`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 
  ```json
  {
    "ai_takeover_enabled": true,
    "reply_delay": 2,
    "min_reply_interval": 60,
    "reply_style": "professional",
    "max_reply_length": 300,
    "contact_person": "文件传输助手",
    "ai_persona": "你是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。",
    "keywords": ["紧急", "重要"],
    "custom_rules": [],
    "reply_template": "您好，{{username}}，关于您的问题，{{response}}"
  }
  ```
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "更新成功",
    "data": {
      "ai_takeover_enabled": true,
      "reply_delay": 2,
      "min_reply_interval": 60,
      "reply_style": "professional",
      "max_reply_length": 300,
      "contact_person": "文件传输助手",
      "ai_persona": "你是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。",
      "keywords": ["紧急", "重要"],
      "custom_rules": [],
      "reply_template": "您好，{{username}}，关于您的问题，{{response}}"
    }
  }
  ```

### AI 历史记录 API

#### 获取 AI 回复历史
- **URL**: `/api/ai-history`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **参数**: 
  - `page` (可选): 页码，默认 1
  - `per_page` (可选): 每页数量，默认 20
  - `start_date` (可选): 开始日期
  - `end_date` (可选): 结束日期
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total": 50,
      "page": 1,
      "per_page": 20,
      "history": [
        {
          "id": 1,
          "user_message": "您好，请问如何设置定时任务？",
          "ai_response": "您好，进入自动信息页面，填写相关信息后点击创建任务即可。",
          "timestamp": "2024-05-20T14:30:00",
          "feedback_rating": 5
        },
        // 更多记录...
      ]
    }
  }
  ```

#### 添加 AI 回复记录
- **URL**: `/api/ai-history`
- **方法**: `POST`
- **请求头**: `Authorization: Bearer <token>`
- **请求体**: 
  ```json
  {
    "user_message": "您好，请问如何设置定时任务？",
    "ai_response": "您好，进入自动信息页面，填写相关信息后点击创建任务即可。",
    "timestamp": "2024-05-20T14:30:00"
  }
  ```
- **响应**: 
  ```json
  {
    "code": 201,
    "message": "添加成功",
    "data": {
      "id": 1,
      "user_message": "您好，请问如何设置定时任务？",
      "ai_response": "您好，进入自动信息页面，填写相关信息后点击创建任务即可。",
      "timestamp": "2024-05-20T14:30:00"
    }
  }
  ```

### 统计分析 API

#### 获取任务统计
- **URL**: `/api/stats/tasks`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **参数**: 
  - `start_date` (可选): 开始日期
  - `end_date` (可选): 结束日期
  - `group_by` (可选): 分组方式 (day/week/month/year)
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total_tasks": 100,
      "completed_tasks": 85,
      "failed_tasks": 15,
      "success_rate": 85,
      "task_trends": [
        {
          "date": "2024-05-01",
          "count": 5
        },
        // 更多趋势数据...
      ],
      "tasks_by_type": [
        {
          "type": "single",
          "count": 40
        },
        {
          "type": "daily",
          "count": 30
        },
        // 更多类型数据...
      ]
    }
  }
  ```

#### 获取 AI 统计
- **URL**: `/api/stats/ai`
- **方法**: `GET`
- **请求头**: `Authorization: Bearer <token>`
- **参数**: 
  - `start_date` (可选): 开始日期
  - `end_date` (可选): 结束日期
- **响应**: 
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "total_replies": 200,
      "avg_response_time": 2.5,
      "avg_response_length": 150,
      "feedback_scores": {
        "1": 5,
        "2": 10,
        "3": 20,
        "4": 60,
        "5": 105
      },
      "reply_trends": [
        {
          "date": "2024-05-01",
          "count": 10
        },
        // 更多趋势数据...
      ]
    }
  }
  ```

### 错误码说明

| 错误码 | 描述 |
|--------|------|
| 200    | 成功 |
| 201    | 创建成功 |
| 400    | 请求参数错误 |
| 401    | 未授权 |
| 403    | 权限不足 |
| 404    | 资源不存在 |
| 500    | 服务器内部错误 |

---

## 🤝 贡献指南

欢迎对 LeafAuto Web 项目进行贡献！无论是代码改进、bug 修复还是文档完善，我们都非常欢迎。

### 贡献步骤
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 代码规范
- 前端代码：遵循 ESLint 和 Prettier 配置
- 后端代码：遵循 PEP 8 规范
- 提交消息：清晰描述变更内容，使用英文
- 文档更新：如有功能变更，请同步更新相关文档

### 报告问题
如果您发现任何问题或有任何建议，请在 GitHub Issues 中提交。

---

## 📜 许可证

本项目采用 [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0) 协议发布。

根据协议，你可以：
- 自由使用、复制和分发本软件
- 修改本软件并分发修改后的版本

但必须遵守以下条款：
- 保留原作者版权声明和许可证信息
- 修改后的版本必须采用相同许可证发布
- 若通过网络提供本软件的服务，必须公开对应的源代码

详情请参阅 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

- **项目主页**：[https://github.com/YangShengzhou03/LeafAutoWeb](https://github.com/YangShengzhou03/LeafAutoWeb)
- **问题反馈**：[提交 Issue](https://github.com/YangShengzhou03/LeafAutoWeb/issues)
- **代码贡献**：[提交 Pull Request](https://github.com/YangShengzhou03/LeafAutoWeb/pulls)
- **商务合作**：3555844679@qq.com（主题注明"LeafAutoWeb 合作"）
- **开发者**：YangShengzhou

© 2024 Yangshengzhou. All rights reserved.
Powered by AGPL-3.0.