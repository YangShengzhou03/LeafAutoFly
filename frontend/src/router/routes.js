import Layout from '@/components/layout/Layout.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Profile from '@/views/profile/Profile.vue'
import TaskList from '@/views/task/TaskList.vue'
import TaskDetail from '@/views/task/TaskDetail.vue'
import TaskCreate from '@/views/task/TaskCreate.vue'
import AiService from '@/views/ai/AiService.vue'
import NotFound from '@/views/errors/NotFound.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
          title: '仪表盘',
          requiresAuth: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: {
          title: '个人资料',
          requiresAuth: true
        }
      },
      {
        path: 'tasks',
        name: 'TaskList',
        component: TaskList,
        meta: {
          title: '任务列表',
          requiresAuth: true
        }
      },
      {
        path: 'tasks/:id',
        name: 'TaskDetail',
        component: TaskDetail,
        meta: {
          title: '任务详情',
          requiresAuth: true
        }
      },
      {
        path: 'tasks/create',
        name: 'TaskCreate',
        component: TaskCreate,
        meta: {
          title: '创建任务',
          requiresAuth: true
        }
      },
      {
        path: 'ai',
        name: 'AiService',
        component: AiService,
        meta: {
          title: 'AI服务',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '登录'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '注册'
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '页面不存在'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

export default routes