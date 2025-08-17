# LeafAuto Web 项目 (Vue 3 重构版)

## 项目概述
这是一个基于Vue 3、Element Plus和Vue Router的单页应用，用于管理自动信息发送任务。本项目是对原有原生HTML/CSS/JS项目的重构版本。

## 技术栈
- **前端框架**：Vue 3 (使用`<script setup>`语法糖)
- **组件库**：Element Plus
- **路由管理**：Vue Router 4
- **状态管理**：Pinia
- **样式处理**：CSS + SCSS

## 项目结构
```
LeafAuto_Web/
├── src/
│   ├── assets/
│   │   ├── css/
│   │   │   └── auto_info.css
│   │   └── images/
│   │       └── empty-tasks.svg
│   ├── components/
│   ├── router/
│   │   └── index.js
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── AutoInfoView.vue
│   │   └── AITakeoverView.vue
│   ├── App.vue
│   └── main.js
├── package.json
└── README.md
```

## 核心功能
1. **任务管理**：创建、编辑、删除自动发送任务
2. **定时发送**：设置任务发送时间和重复规则
3. **AI接管**：配置AI自动回复消息的参数和策略
4. **数据统计**：查看任务执行统计信息

## 安装与运行
1. 安装依赖
```bash
npm install
```
2. 运行开发服务器
```bash
npm run serve
```
3. 构建生产环境
```bash
npm run build
```

## 重构要点
1. **组件化**：将原有的HTML结构拆分为多个Vue组件
2. **响应式数据**：使用Vue 3的`ref`和`reactive`替代原生JS的数据操作
3. **表单处理**：使用Element Plus的表单组件替代原生表单
4. **路由管理**：使用Vue Router实现页面导航
5. **样式复用**：保留原项目的CSS样式，确保视觉一致性

## 注意事项
- 确保已安装Node.js和npm
- 开发环境需要支持ES6+语法
- 项目依赖的API接口需要单独部署