<template>
  <div class="tab-header">
    <button
      v-for="item in options"
      :key="item.value"
      type="button"
      :class="['tab-btn', { active: value === item.value }]"
      @click="$emit('input', item.value)"
    >
      {{ item.label }}
    </button>
    <div class="tab-indicator" :style="{ transform: indicatorTransform }"></div>
  </div>
</template>

<script>
export default {
  name: 'HmTabSwitch',
  props: {
    value: { type: String, required: true },
    options: {
      type: Array,
      default: () => ([
        { label: '账号登录', value: 'login' },
        { label: '注册账号', value: 'register' }
      ])
    }
  },
  computed: {
    indicatorTransform() {
      const index = this.options.findIndex((item) => item.value === this.value)
      const safeIndex = index < 0 ? 0 : index
      return `translateX(${safeIndex * 100}%)`
    }
  }
}
</script>

<style scoped>
.tab-header {
  display: flex;
  position: relative;
  width: 300px;
  background: linear-gradient(160deg, #9b8263, #5f4933);
  border-radius: 14px;
  padding: 4px;
  margin: 0 auto 36px;
  box-shadow:
    0 6px 0 #3a2e22,
    0 8px 12px rgba(0, 0, 0, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.22);
  overflow: hidden;
}

.tab-btn {
  flex: 1;
  padding: 11px 0;
  border: none;
  background: transparent;
  font-size: 12px;
  font-weight: bold;
  font-family: 'Courier New', monospace;
  color: #f5e6cc;
  cursor: pointer;
  position: relative;
  z-index: 3;
  letter-spacing: 1.5px;
  text-shadow:
    0 1px 3px rgba(0, 0, 0, 0.7),
    0 0 8px rgba(255, 220, 150, 0.25);
  transition: color 0.3s;
}

.tab-btn.active {
  color: #ffe8b0;
}

.tab-indicator {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: linear-gradient(180deg, #947552 0%, #5a412d 100%);
  border-radius: 10px;
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.5),
    inset 0 -1px 2px rgba(255, 255, 255, 0.12),
    0 2px 4px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 2;
}

.tab-indicator::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.16), transparent);
  border-radius: 10px 10px 0 0;
}
</style>
