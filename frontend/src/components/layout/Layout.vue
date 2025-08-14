<template>
  <div class="app-container">
    <el-container style="height: 100vh; overflow: hidden;">
      <!-- 侧边栏 -->
      <el-aside
        :width="isCollapse ? '64px' : '200px'"
        style="background-color: #001529; transition: width 0.3s;"
        :class="{ 'aside-collapsed': isCollapse }"
      >
        <div class="logo-container">
          <div class="logo">
            <img src="@/assets/images/logo.png" alt="Logo" v-if="!isCollapse" />
            <span v-if="!isCollapse" class="logo-text">LeafAuto</span>
          </div>
          <el-button
            @click="toggleCollapse"
            size="mini"
            class="toggle-button"
            :icon="isCollapse ? Expand : Fold"
          />
        </div>
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#ffd04b"
          :collapse="isCollapse"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><PieChart /></el-icon>
            <span slot="title">仪表盘</span>
          </el-menu-item>
          <el-menu-item index="tasks">
            <el-icon><List /></el-icon>
            <span slot="title">任务管理</span>
          </el-menu-item>
          <el-menu-item index="ai">
            <el-icon><Cpu /></el-icon>
            <span slot="title">AI服务</span>
          </el-menu-item>
          <el-menu-item index="profile">
            <el-icon><User /></el-icon>
            <span slot="title">个人资料</span>
          </el-menu-item>
          <el-menu-item index="logout">
            <el-icon><Logout /></el-icon>
            <span slot="title">退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header style="padding: 0; background-color: #fff; border-bottom: 1px solid #eee;">
          <div class="header-container">
            <div class="user-info">
              <el-avatar :size="36" class="avatar">
                <UserFilled />
              </el-avatar>
              <span class="username">{{ username }}</span>
            </div>
            <div class="header-actions">
              <el-dropdown trigger="click">
                <el-icon class="header-icon"><Bell /></el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>通知 1</el-dropdown-item>
                    <el-dropdown-item>通知 2</el-dropdown-item>
                    <el-dropdown-item>通知 3</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown trigger="click">
                <el-icon class="header-icon"><Setting /></el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>设置</el-dropdown-item>
                    <el-dropdown-item>主题</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>

        <!-- 主内容区 -->
        <el-main style="padding: 20px; overflow: auto;">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PieChart, List, Cpu, User, Logout, Expand, Fold, Bell, Setting, UserFilled }
  from '@element-plus/icons-vue'

// 响应式数据
const isCollapse = ref(false)
const username = ref('管理员')
const route = useRoute()
const router = useRouter()

// 计算当前激活的菜单
const activeMenu = computed(() => {
  const path = route.path
  if (path.includes('dashboard')) return 'dashboard'
  if (path.includes('tasks')) return 'tasks'
  if (path.includes('ai')) return 'ai'
  if (path.includes('profile')) return 'profile'
  return 'dashboard'
})

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 处理菜单选择
const handleMenuSelect = (key) => {
  switch (key) {
    case 'dashboard':
      router.push('/dashboard')
      break
    case 'tasks':
      router.push('/tasks')
      break
    case 'ai':
      router.push('/ai')
      break
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      // 这里可以添加退出登录逻辑
      router.push('/login')
      break
  }
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  overflow: hidden;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}

.logo-text {
  color: #fff;
  font-size: 16px;
  font-weight: bold;
}

.toggle-button {
  background-color: transparent;
  color: #fff;
  border: none;
}

.el-menu-vertical-demo {
  width: 100%;
  height: calc(100% - 60px);
  overflow-y: auto;
}

.aside-collapsed .el-menu {
  width: 64px;
}

.main-container {
  width: 100%;
  overflow: hidden;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  margin-right: 10px;
}

.username {
  font-size: 14px;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
}

.header-icon {
  font-size: 18px;
  margin-left: 20px;
  color: #666;
  cursor: pointer;
}

.header-icon:hover {
  color: #1890ff;
}
</style>