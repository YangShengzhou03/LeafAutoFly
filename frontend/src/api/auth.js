import client from './client'

export default {
  /**
   * 用户登录
   * @param {string} username - 用户名
   * @param {string} password - 密码
   */
  login(username, password) {
    return client.post('/auth/login', { username, password })
  },
  
  /**
   * 用户注册
   * @param {Object} userData - 用户数据
   */
  register(userData) {
    return client.post('/auth/register', userData)
  },
  
  /**
   * 用户登出
   */
  logout() {
    return client.post('/auth/logout')
  },
  
  /**
   * 获取当前用户信息
   */
  getProfile() {
    return client.get('/auth/profile')
  },
  
  /**
   * 更新用户信息
   * @param {Object} userData - 要更新的用户数据
   */
  updateProfile(userData) {
    return client.put('/auth/profile', userData)
  },
  
  /**
   * 修改密码
   * @param {string} oldPassword - 旧密码
   * @param {string} newPassword - 新密码
   */
  changePassword(oldPassword, newPassword) {
    return client.post('/auth/change-password', { oldPassword, newPassword })
  }
}
