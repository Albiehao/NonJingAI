import Vue from 'vue'

const ToastService = {
  instance: null,
  init(instance) {
    this.instance = instance
  },
  success(msg, duration = 2000) {
    if (this.instance) this.instance.success(msg, duration)
  },
  error(msg, duration = 2000) {
    if (this.instance) this.instance.error(msg, duration)
  },
  warning(msg, duration = 2000) {
    if (this.instance) this.instance.warning(msg, duration)
  },
  info(msg, duration = 2000) {
    if (this.instance) this.instance.show(msg, duration, 'info')
  }
}

// 挂载到 Vue 和 window，方便路由守卫使用
Vue.prototype.$toast = ToastService
window.$toast = ToastService

export default ToastService