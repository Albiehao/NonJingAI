import Vue from 'vue'
import App from './App.vue'
import RadioPanel from './components/common/RadioPanel.vue'
import HmButton from './components/common/HmButton.vue'
import router from './router'
import './styles/reset.css'
import './utils/toast'

Vue.config.productionTip = false
Vue.component('radio-panel', RadioPanel)
Vue.component('hm-button', HmButton)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
