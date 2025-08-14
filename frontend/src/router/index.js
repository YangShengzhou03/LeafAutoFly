import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局导航守卫
router.beforeEach((to, from, next) => {
  // 可以在这里添加认证逻辑
  next()
})

router.afterEach(() => {
  // 可以在这里添加页面加载完成后的逻辑
})

export default router