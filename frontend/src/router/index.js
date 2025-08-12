import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import ExampleList from '@/views/examples/List.vue'
import ExampleCreate from '@/views/examples/Create.vue'
import ExampleEdit from '@/views/examples/Edit.vue'
import About from '@/views/About.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Profile from '@/views/user/Profile.vue'
import ChangePassword from '@/views/user/ChangePassword.vue'
import NotFound from '@/views/errors/404.vue'
import Forbidden from '@/views/errors/403.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/examples',
    name: 'ExampleList',
    component: ExampleList,
    meta: {
      title: '示例数据列表',
      requiresAuth: true
    }
  },
  {
    path: '/examples/create',
    name: 'ExampleCreate',
    component: ExampleCreate,
    meta: {
      title: '创建示例数据',
      requiresAuth: true
    }
  },
  {
    path: '/examples/:id/edit',
    name: 'ExampleEdit',
    component: ExampleEdit,
    meta: {
      title: '编辑示例数据',
      requiresAuth: true
    },
    props: true
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: '关于我们'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '用户登录',
      guestOnly: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '用户注册',
      guestOnly: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      title: '个人资料',
      requiresAuth: true
    }
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: {
      title: '修改密码',
      requiresAuth: true
    }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: Forbidden,
    meta: {
      title: '访问被拒绝'
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '页面未找到'
    }
  },
  // 通配符路由，匹配所有未定义的路由
  {
    path: '*',
    redirect: '/404'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 页面滚动行为
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})

// 路由守卫：验证权限
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user') !== null;
  
  // 需要登录但未登录的情况
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } 
  // 已登录但访问登录/注册页的情况
  else if (to.meta.guestOnly && isAuthenticated) {
    next('/');
  } 
  // 其他情况正常访问
  else {
    next();
  }
});

// 路由后置钩子，设置页面标题
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - LeafAuto` : 'LeafAuto';
});

export default router
