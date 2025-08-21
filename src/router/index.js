import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../views/AppLayout.vue'
import HomeView from '../views/HomeView.vue'
import AutoInfoView from '../views/AutoInfoView.vue'
import AITakeoverView from '../views/AITakeoverView.vue'
import DataExportView from '../views/DataExportView.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      { path: '', name: 'home', component: HomeView },
      { path: 'auto_info', name: 'auto_info', component: AutoInfoView },
      { path: 'ai_takeover', name: 'ai_takeover', component: AITakeoverView },
      { path: 'data_export', name: 'data_export', component: DataExportView },
      { path: 'data_export', name: 'data_export', component: DataExportView },
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