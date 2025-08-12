import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import examples from './modules/examples'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    examples
  },
  getters: {
    isAuthenticated: state => state.auth.isAuthenticated
  }
})
