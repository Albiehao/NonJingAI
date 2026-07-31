import Vue from 'vue'
import AdminShell from './AdminShell.vue'
import '../../styles/reset.css'

Vue.config.productionTip = false

new Vue({
  render: (h) => h(AdminShell)
}).$mount('#app')
