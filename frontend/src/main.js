import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'

// 导入全局样式
import './assets/styles/index.scss'

// 导入Axios配置
import './utils/axios'

// 导入全局组件
import BaseButton from './components/BaseButton.vue'
import BaseCard from './components/BaseCard.vue'
import Loading from './components/Loading.vue'

// 注册全局组件
Vue.component('BaseButton', BaseButton)
Vue.component('BaseCard', BaseCard)
Vue.component('Loading', Loading)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
