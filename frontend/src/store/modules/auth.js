import authApi from '@/api/auth'

const state = {
  user: JSON.parse(localStorage.getItem('user')),
  token: localStorage.getItem('token'),
  loading: false,
  error: null
}

const getters = {
  isAuthenticated: state => !!state.user,
  currentUser: state => state.user,
  authLoading: state => state.loading,
  authError: state => state.error
}

const mutations = {
  setUser(state, user) {
    state.user = user;
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  },
  setToken(state, token) {
    state.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  setError(state, error) {
    state.error = error;
  }
}

const actions = {
  async login({ commit }, { username, password }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await authApi.login(username, password);
      commit('setUser', response.data.user);
      commit('setToken', 'dummy-token'); // 在实际应用中使用真实token
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '登录失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async register({ commit }, userData) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await authApi.register(userData);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '注册失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async logout({ commit }) {
    commit('setLoading', true);
    
    try {
      await authApi.logout();
      commit('setUser', null);
      commit('setToken', null);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      commit('setLoading', false);
    }
  },
  
  async fetchProfile({ commit }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await authApi.getProfile();
      commit('setUser', response.data.user);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '获取个人信息失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async updateProfile({ commit }, userData) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await authApi.updateProfile(userData);
      commit('setUser', response.data.user);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '更新个人信息失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async changePassword({ commit }, { oldPassword, newPassword }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await authApi.changePassword(oldPassword, newPassword);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '修改密码失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
