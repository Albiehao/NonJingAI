<template>
  <transition name="toast-fade">
    <div v-if="visible" class="toast-container" :class="type">
      <span class="toast-message">{{ message }}</span>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'ToastMessage',
  data() {
    return {
      visible: false,
      message: '',
      type: 'info'
    }
  },
  methods: {
    show(msg, duration = 2000, type = 'info') {
      this.message = msg
      this.type = type
      this.visible = true
      setTimeout(() => {
        this.visible = false
      }, duration)
    },
    success(msg, duration = 2000) {
      this.show(msg, duration, 'success')
    },
    error(msg, duration = 2000) {
      this.show(msg, duration, 'error')
    },
    warning(msg, duration = 2000) {
      this.show(msg, duration, 'warning')
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 4px;
  z-index: 9999;
  font-size: 14px;
  font-family: 'Courier New', monospace;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.toast-container.success {
  background: #2d5a27;
  color: #e8f5e8;
  border: 1px solid #4a7c4a;
}

.toast-container.error {
  background: #5a2727;
  color: #f5e8e8;
  border: 1px solid #7c4a4a;
}

.toast-container.warning {
  background: #5a4a27;
  color: #f5e8d8;
  border: 1px solid #7c6a4a;
}

.toast-container.info {
  background: #27405a;
  color: #e8f0f8;
  border: 1px solid #4a6a7c;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.3s ease;
}

.toast-fade-enter,
.toast-fade-leave-to {
  opacity: 0;
}
</style>