import axios from 'axios'
import store from '@/store'
import router from '@/router'

// 创建Axios实例
const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    // 添加认证令牌
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      // 清除用户信息并跳转到登录页
      store.dispatch('auth/logout').then(() => {
        router.push('/login')
      })
    }
    
    return Promise.reject(error)
  }
)

// 全局注册Axios
window.axios = instance

export default instance
