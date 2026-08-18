<template>
  <div class="device-page">
    <div class="page-header">
      <div>
        <h1>MQTT 设备</h1>
        <p>通过设备 SN 和设备密码绑定硬件。当前阶段仅管理绑定关系，不处理设备业务数据。</p>
      </div>
      <a-button type="primary" @click="openBindModal">绑定设备</a-button>
    </div>

    <a-card :bordered="false" class="device-card">
      <a-spin :spinning="loading">
        <a-empty v-if="!loading && devices.length === 0" description="暂未绑定设备" />

        <div v-else class="device-list">
          <div v-for="item in devices" :key="item.sn" class="device-item">
            <div class="device-main">
              <div class="device-icon">
                <RadioTower :size="22" />
              </div>
              <div>
                <div class="device-sn">{{ item.sn }}</div>
                <div class="device-meta">
                  MQTT Username / ClientId：{{ item.sn }}
                  <span v-if="item.created_at"> · 绑定于 {{ formatTime(item.created_at) }}</span>
                </div>
              </div>
            </div>

            <a-popconfirm
              title="确认解绑这台设备？"
              ok-text="解绑"
              cancel-text="取消"
              @confirm="handleUnbind(item.sn)"
            >
              <a-button danger type="text">解绑</a-button>
            </a-popconfirm>
          </div>
        </div>
      </a-spin>
    </a-card>

    <a-modal
      v-model:open="bindVisible"
      title="绑定 MQTT 设备"
      ok-text="绑定"
      cancel-text="取消"
      :confirm-loading="binding"
      @ok="handleBind"
      @cancel="resetForm"
    >
      <a-form layout="vertical" class="bind-form">
        <a-form-item label="设备 SN" required>
          <a-input
            v-model:value="form.sn"
            placeholder="请输入设备 SN"
            autocomplete="off"
            @press-enter="handleBind"
          />
          <div class="field-help">SN 同时作为 MQTT Username 和 ClientId。</div>
        </a-form-item>

        <a-form-item label="设备密码" required>
          <a-input-password
            v-model:value="form.password"
            placeholder="请输入设备 MQTT 密码"
            autocomplete="new-password"
            @press-enter="handleBind"
          />
          <div class="field-help">密码仅用于本次设备凭据验证，主系统不会保存 MQTT 明文密码。</div>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import { RadioTower } from 'lucide-vue-next'
import { bindDevice, getBoundDevices, unbindDevice } from '@/apis/device_api'

const loading = ref(false)
const binding = ref(false)
const bindVisible = ref(false)
const devices = ref([])
const form = reactive({
  sn: '',
  password: ''
})

const formatTime = (value) => {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

const loadDevices = async () => {
  loading.value = true
  try {
    devices.value = (await getBoundDevices()) || []
  } catch (error) {
    message.error(error.message || '加载设备失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.sn = ''
  form.password = ''
}

const openBindModal = () => {
  resetForm()
  bindVisible.value = true
}

const handleBind = async () => {
  const sn = form.sn.trim()
  if (!sn || !form.password) {
    message.warning('请输入设备 SN 和设备密码')
    return
  }

  binding.value = true
  try {
    const result = await bindDevice(sn, form.password)
    message.success(result?.message || '绑定成功')
    bindVisible.value = false
    resetForm()
    await loadDevices()
  } catch (error) {
    message.error(error.message || '绑定失败')
  } finally {
    binding.value = false
  }
}

const handleUnbind = async (sn) => {
  try {
    const result = await unbindDevice(sn)
    message.success(result?.message || '解绑成功')
    await loadDevices()
  } catch (error) {
    message.error(error.message || '解绑失败')
  }
}

onMounted(loadDevices)
</script>

<style lang="less" scoped>
.device-page {
  padding: 28px;
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 6px;
  font-size: 24px;
  font-weight: 600;
  color: var(--gray-1000);
}

.page-header p {
  margin: 0;
  color: var(--gray-600);
  font-size: 14px;
}

.device-card {
  border-radius: 12px;
}

.device-list {
  display: flex;
  flex-direction: column;
}

.device-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 16px 4px;
  border-bottom: 1px solid var(--gray-100);
}

.device-item:last-child {
  border-bottom: 0;
}

.device-main {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.device-icon {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--main-40);
  color: var(--main-color);
  flex: 0 0 auto;
}

.device-sn {
  font-size: 15px;
  font-weight: 600;
  color: var(--gray-1000);
  word-break: break-all;
}

.device-meta,
.field-help {
  margin-top: 4px;
  font-size: 12px;
  color: var(--gray-500);
}

.bind-form {
  padding-top: 8px;
}

@media (max-width: 640px) {
  .device-page {
    padding: 18px;
  }

  .page-header {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
