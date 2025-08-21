import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../views/AppLayout.vue'
import HomeView from '../views/HomeView.vue'
import AutoInfoView from '../views/AutoInfoView.vue'
import AITakeoverView from '../views/AITakeoverView.vue'
import OtherBoxView from '../views/OtherBoxView.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      { path: '', name: 'home', component: HomeView },
      { path: 'auto_info', name: 'auto_info', component: AutoInfoView },
      { path: 'ai_takeover', name: 'ai_takeover', component: AITakeoverView },
      { path: 'other_box', name: 'other_box', component: OtherBoxView },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  next()
})

export default router