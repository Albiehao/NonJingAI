<template>
  <div class="time-view-container">
    <!-- 页面标题 -->
    <header class="page-header">
      <h2>定时任务管理</h2>
    </header>

    <!-- 内容区域 -->
    <main class="content-area">
      <!-- 第4步：触发按钮 -->
      <div class="action-bar">
        <button class="add-btn" @click="showTimerModal = true">
          + 新建定时任务
        </button>
      </div>

      <!-- 任务列表占位符 (以后在这里展示数据) -->
      <div class="list-placeholder">
        <p>暂无定时任务，请点击上方按钮添加。</p>
      </div>
    </main>

    <!-- 第3步：放置组件标签 -->
    <!-- 放在模板最后，绑定 visible 和 confirm 事件 -->
    <TimerConfigModal
        v-model:visible="showTimerModal"
        @confirm="handleSaveTimer"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
// 第1步：引入组件
import TimerConfigModal from '@/components/TimerConfigModal.vue'

// 第2步：定义开关变量
const showTimerModal = ref(false)

// 处理保存定时的函数
const handleSaveTimer = (data) => {
  console.log('收到定时配置数据:', data)
  // TODO: 这里调用后端接口保存数据
  alert('配置已提交！(请查看控制台输出)')
}
</script>

<style scoped>
.time-view-container {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.action-bar {
  margin-bottom: 20px;
}

.add-btn {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.add-btn:hover {
  background-color: #40a9ff;
}

.list-placeholder {
  text-align: center;
  color: #999;
  margin-top: 50px;
}
</style>