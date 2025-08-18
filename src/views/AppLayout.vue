<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="top-section">
        <div class="user-info">
          <div class="avatar">枫</div>
          <span class="unlogin">未登录</span>
        </div>
        <nav class="menu">
          <ul>
            <li class="menu-item" :class="{ active: currentRoute === '/' }">
              <router-link to="/">首页</router-link>
            </li>
            <li class="menu-item" :class="{ active: currentRoute === '/auto_info' }">
              <router-link to="/auto_info">自动信息</router-link>
            </li>
            <li class="menu-item" :class="{ active: currentRoute === '/ai_takeover' }">
              <router-link to="/ai_takeover">AI 运营</router-link>
            </li>
          </ul>
        </nav>
      </div>
      <div class="sidebar-footer">
        <div class="dev-info">开发时间 2.458 / 10GB</div>
        <button class="upgrade-btn">升级专业版</button>
      </div>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRoute, onBeforeRouteUpdate } from 'vue-router';
import { ref } from 'vue';

const route = useRoute();
const currentRoute = ref(route.path);

onBeforeRouteUpdate((to) => {
  currentRoute.value = to.path;
});
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

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
  background-color: #4361ee;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 8px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.15);
}

.avatar:hover {
  transform: scale(1.05) rotate(5deg);
  box-shadow: 0 6px 16px rgba(67, 97, 238, 0.25);
  background-color: #3a56d4;
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
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.menu {
  width: 100%;
  padding: 0 1rem;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.menu-item {
  margin-bottom: 0.5rem;
  border-radius: 8px;
  transition: var(--transition);
  width: 100%;
  text-align: center;
  position: relative;
  cursor: pointer;
}

.menu-item a {
  color: var(--text-primary);
  text-decoration: none;
  display: block;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: var(--transition);
  font-size: 16px;
  width: 100%;
  height: 100%;
}

.menu-item:hover {
  background-color: rgba(67, 97, 238, 0.08);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.1);
}

.menu-item.active {
  background-color: rgba(67, 97, 238, 0.12);
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.15);
}

.menu-item.active a {
  color: var(--primary-color);
  font-weight: 600;
}

.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: var(--primary-color);
  border-radius: 0 4px 4px 0;
}

.sidebar-footer {
  width: 100%;
  padding: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
  text-align: center;
}

.dev-info {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.4;
}

.upgrade-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: var(--transition);
  width: 100%;
  max-width: 160px;
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.25);
}

.upgrade-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

.main-content {
  flex: 1;
  padding: 12px;
  box-sizing: border-box;
  overflow-y: auto;
  background-color: #fafafa;
  min-height: 100vh;
}

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
