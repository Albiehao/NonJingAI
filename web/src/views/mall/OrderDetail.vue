<template>
  <div class="mall-page">
    <div class="page-header">
      <h1>订单详情</h1>
      <p class="subtitle">订单 ID: {{ $route.params.id }}，内容待填充。</p>
    </div>
    <div class="page-content">
      <a-empty description="暂无订单详情" />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style lang="less" scoped>
.mall-page {
  padding: 24px;
  min-height: 100%;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: var(--gray-500);
}

.page-content {
  background: #fff;
  border-radius: 8px;
  padding: 48px;
  min-height: 400px;
}
</style>
