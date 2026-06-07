<template>
  <div class="share-config-form">
    <div class="share-config-content">
      <p class="share-hint">所有用户都可以访问</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({
      is_shared: true
    })
  }
})

const emit = defineEmits(['update:modelValue'])

// 本地状态，固定为全员共享模式
const config = reactive({
  is_shared: true
})

// 初始化并同步到父组件
onMounted(() => {
  emit('update:modelValue', {
    is_shared: true
  })
})

// 暴露方法给父组件
defineExpose({
  config,
  validate: () => ({ valid: true, message: '' })
})
</script>

<style lang="less" scoped>
.share-config-form {
  .share-config-content {
    background: var(--gray-25);
    border-radius: 8px;
    padding: 16px;
    border: 1px solid var(--gray-150);

    .share-hint {
      font-size: 13px;
      color: var(--gray-600);
      margin: 0;
    }
  }
}
</style>
