import examplesApi from '@/api/examples'

const state = {
  examples: [],
  currentExample: null,
  loading: false,
  error: null
}

const getters = {
  allExamples: state => state.examples,
  currentExample: state => state.currentExample,
  examplesLoading: state => state.loading,
  examplesError: state => state.error
}

const mutations = {
  setExamples(state, examples) {
    state.examples = examples;
  },
  setCurrentExample(state, example) {
    state.currentExample = example;
  },
  addExample(state, example) {
    state.examples.push(example);
  },
  updateExample(state, updatedExample) {
    const index = state.examples.findIndex(e => e.id === updatedExample.id);
    if (index !== -1) {
      state.examples.splice(index, 1, updatedExample);
    }
    
    if (state.currentExample && state.currentExample.id === updatedExample.id) {
      state.currentExample = updatedExample;
    }
  },
  removeExample(state, exampleId) {
    state.examples = state.examples.filter(e => e.id !== exampleId);
    
    if (state.currentExample && state.currentExample.id === exampleId) {
      state.currentExample = null;
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
  async fetchExamples({ commit }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await examplesApi.getAllExamples();
      commit('setExamples', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '获取示例数据失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async fetchMyExamples({ commit }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await examplesApi.getMyExamples();
      commit('setExamples', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '获取我的示例数据失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async fetchExampleById({ commit }, exampleId) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await examplesApi.getExampleById(exampleId);
      commit('setCurrentExample', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '获取示例数据失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async createExample({ commit }, exampleData) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await examplesApi.createExample(exampleData);
      commit('addExample', response.data.example);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '创建示例数据失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async updateExample({ commit }, { exampleId, exampleData }) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      const response = await examplesApi.updateExample(exampleId, exampleData);
      commit('updateExample', response.data.example);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || '更新示例数据失败');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  
  async deleteExample({ commit }, exampleId) {
    commit('setLoading', true);
    commit('setError', null);
    
    try {
      await examplesApi.deleteExample(exampleId);
      commit('removeExample', exampleId);
      return true;
    } catch (error) {
      commit('setError', error.response?.data?.message || '删除示例数据失败');
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
