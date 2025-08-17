<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <div class="user-info">
        <div class="avatar"></div>
        <span class="unlogin">未登录</span>
      </div>
      <nav class="menu">
        <ul>
          <li class="menu-item" :class="{ active: currentRoute === '/' }">
            <a href="#" @click.prevent="navigateTo('/')">首页</a>
          </li>
          <li class="menu-item" :class="{ active: currentRoute === '/auto_info' }">
            <a href="#" @click.prevent="navigateTo('/auto_info')">自动信息</a>
          </li>
          <li class="menu-item" :class="{ active: currentRoute === '/ai_takeover' }">
            <a href="#" @click.prevent="navigateTo('/ai_takeover')">AI 运营</a>
          </li>
        </ul>
      </nav>
      <div class="sidebar-footer">
        <div class="dev-info">开发时间 2.458 / 10GB</div>
        <button class="upgrade-btn">升级专业版</button>
      </div>
    </aside>

    <!-- 右侧主体内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();
const route = useRoute();
const currentRoute = ref(route.path);

// 导航到指定路由
const navigateTo = (path) => {
  router.push(path);
};

// 监听路由变化
onBeforeRouteUpdate((to) => {
  currentRoute.value = to.path;
});
</script>

<style scoped>
.app-layout {
  display: flex;
}

/* 左侧导航栏样式 */
.sidebar {
  width: calc(100% / 8);
  background: linear-gradient(to bottom, #f5f7fa, #e4e6eb);
  padding: 24px 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #e4e6eb;
  border: 2px solid #d0d3d9;
  margin-bottom: 8px;
}

.unlogin {
  color: #666;
  font-size: 14px;
}

.menu {
  width: 100%;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  width: 100%;
  text-align: center;
  padding: 12px 0;
  position: relative;
  cursor: pointer;
}

.menu-item:not(:last-child)::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 15%;
  width: 70%;
  height: 1px;
  background-color: #d0d3d9;
}

.menu-item a {
  text-decoration: none;
  color: #999;
  font-size: 16px;
  transition: color 0.3s;
  display: block;
  width: 100%;
  height: 100%;
}

.menu-item.active {
  background: linear-gradient(to right, rgba(216, 180, 254, 0.5), rgba(216, 180, 254, 0));
}

.menu-item.active a {
  color: #333;
}

.sidebar-footer {
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.dev-info {
  color: #666;
  font-size: 12px;
  text-align: center;
}

.upgrade-btn {
  background: linear-gradient(to right, #9333ea, #c084fc);
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(147, 51, 234, 0.2);
  font-size: 14px;
  width: 100%;
  max-width: 140px;
}

.upgrade-btn:hover {
  background: linear-gradient(to right, #c084fc, #9333ea);
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(147, 51, 234, 0.3);
}

/* 右侧主体内容区样式 */
.main-content {
  width: calc(100% * 7 / 8);
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
  margin-left: calc(100% / 8);
  min-height: 100vh;
}
</style>