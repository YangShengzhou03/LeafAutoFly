<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-aside width="200px" style="background-color: #f0f2f5; box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);">
        <div class="logo-container" style="height: 60px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #e6e6e6;">
          <h2 style="color: #1890ff; margin: 0;">LeafAuto Web</h2>
        </div>
        <el-menu
          default-active="/"
          class="el-menu-vertical-demo"
          @select="handleMenuSelect"
          background-color="#f0f2f5"
          text-color="#333"
          active-text-color="#1890ff"
        >
          <el-menu-item index="/">
            <i class="el-icon-s-home" slot="title"></i>
            <span slot="title">首页</span>
          </el-menu-item>
          <el-menu-item index="/auto_info">
            <i class="el-icon-s-flag" slot="title"></i>
            <span slot="title">自动信息</span>
          </el-menu-item>
          <el-menu-item index="/ai_takeover">
            <i class="el-icon-s-comment" slot="title"></i>
            <span slot="title">AI接管</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="height: 60px; padding: 0 20px; border-bottom: 1px solid #e6e6e6; background-color: #fff; display: flex; align-items: center; justify-content: flex-end;">
          <div style="color: #333;">欢迎使用 LeafAuto Web</div>
        </el-header>
        <el-main style="padding: 20px; background-color: #f7f8fa;">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { ElMenu, ElMenuItem, ElContainer, ElAside, ElHeader, ElMain } from 'element-plus';

const router = useRouter();
const currentRoute = ref('');

// 处理菜单选择
const handleMenuSelect = (index) => {
  router.push(index);
};

// 初始化当前路由
onMounted(() => {
  currentRoute.value = router.currentRoute.value.path;
});
</script>

<style scoped>
#app {
  height: 100%;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
}

.el-menu {
  border-right: none;
}

.logo-container {
  background-color: #1890ff;
}

.logo-container h2 {
  color: white;
}
</style>