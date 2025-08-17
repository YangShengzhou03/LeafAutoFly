<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <div class="top-section">
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
      </div>
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

const navigateTo = (path) => router.push(path);

onBeforeRouteUpdate((to) => {
  currentRoute.value = to.path;
});
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

/* 左侧导航栏样式 */
.sidebar {
  width: 220px;
  background: white;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  padding: 8px 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100vh;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 10;
  transition: all 0.3s ease;
  border-right: 1px solid #f0f0f0;
  border-radius: 0 12px 12px 0;
}

.top-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
  padding-top: 16px;
  padding-bottom: 16px;
  border-bottom: none;
  width: 100%;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #f5f7fa;
  border: 2px solid #e4e6eb;
  margin-bottom: 8px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.05), rgba(192, 132, 252, 0.05));
}

.unlogin {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.menu {
  width: 100%;
  padding: 0 16px;
  margin-top: 0;
  box-sizing: border-box;
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
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.menu-item:hover {
  background-color: #f9fafb;
  transform: translateX(3px);
}

.menu-item a {
  text-decoration: none;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s;
  display: block;
  width: 100%;
  height: 100%;
}

.menu-item.active {
  background: linear-gradient(to right, rgba(216, 180, 254, 0.2), rgba(216, 180, 254, 0));
}

.menu-item.active a {
  color: #9333ea;
}

.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: linear-gradient(to bottom, #9333ea, #c084fc);
  border-radius: 0 4px 4px 0;
}

.sidebar-footer {
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.dev-info {
  color: #666;
  font-size: 12px;
  text-align: center;
  line-height: 1.4;
}

.upgrade-btn {
  background: linear-gradient(to right, #9333ea, #c084fc);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(147, 51, 234, 0.25);
  font-size: 14px;
  font-weight: 500;
  width: 100%;
  max-width: 160px;
}

.upgrade-btn:hover {
  background: linear-gradient(to right, #c084fc, #9333ea);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
}

/* 右侧主体内容区样式 */
.main-content {
  flex: 1;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
  background-color: #fafafa;
  min-height: 100vh;
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .sidebar {
    width: 180px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 160px;
  }
  
  .menu-item a {
    font-size: 14px;
  }
}
</style>
