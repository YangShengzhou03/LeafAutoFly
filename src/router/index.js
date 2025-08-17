import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AutoInfoView from '../views/AutoInfoView.vue'
import AITakeoverView from '../views/AITakeoverView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/auto_info',
    name: 'auto_info',
    component: AutoInfoView
  },
  {
    path: '/ai_takeover',
    name: 'ai_takeover',
    component: AITakeoverView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // 可以在这里添加路由守卫逻辑
  next()
})

export default router