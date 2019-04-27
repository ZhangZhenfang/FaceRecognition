// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import Qs from 'qs'

axios.defaults.withCredentials = true
Vue.use(ElementUI)
Vue.prototype.axios = axios
Vue.prototype.qs = Qs
Vue.prototype.vue = Vue

Vue.config.productionTip = false
axios.interceptors.response.use(function (response) {
  if (response.data.status === 0) {
    console.log('qwer')
    router.push('/login')
    return response
  } else {
    return response
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
