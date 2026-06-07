<template>
  <div class="email-settings-section">
    <h3 class="section-title">邮件服务配置</h3>
    <p class="section-desc">配置 SMTP 邮件服务，用于发送验证码和系统通知。修改后需保存方可生效。</p>

    <div class="settings-form">
      <div class="form-item">
        <label class="form-label">SMTP 服务器</label>
        <a-input
          v-model:value="form.smtp_host"
          placeholder="smtp.qq.com"
        />
        <span class="form-hint">SMTP 服务器地址，如 smtp.qq.com</span>
      </div>

      <div class="form-item">
        <label class="form-label">SMTP 端口</label>
        <a-input-number
          v-model:value="form.smtp_port"
          placeholder="465"
          :min="1"
          :max="65535"
          style="width: 200px"
        />
        <span class="form-hint">SMTP 服务器端口，QQ邮箱使用 465（SSL）</span>
      </div>

      <div class="form-item">
        <label class="form-label">邮箱账号</label>
        <a-input
          v-model:value="form.smtp_user"
          placeholder="your@qq.com"
        />
        <span class="form-hint">发件邮箱账号</span>
      </div>

      <div class="form-item">
        <label class="form-label">邮箱授权码</label>
        <a-input-password
          v-model:value="form.smtp_password"
          placeholder="请输入授权码"
        />
        <span class="form-hint">SMTP 授权码（非登录密码），需在邮箱设置中获取</span>
      </div>

      <div class="form-item">
        <label class="form-label">发件人名称</label>
        <a-input
          v-model:value="form.smtp_from_name"
          placeholder="千寻农业助手"
        />
        <span class="form-hint">收件人看到的发件人名称</span>
      </div>

      <div class="form-item">
        <label class="form-label">发件人邮箱</label>
        <a-input
          v-model:value="form.smtp_from_email"
          placeholder="留空则使用邮箱账号"
        />
        <span class="form-hint">可自定义发件人邮箱地址，留空则使用邮箱账号</span>
      </div>

      <div class="form-actions">
        <a-button type="primary" :loading="saving" @click="handleSave">保存配置</a-button>
        <a-button :loading="testing" @click="handleTest">发送测试邮件</a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useConfigStore } from '@/stores/config'
import { useUserStore } from '@/stores/user'

const configStore = useConfigStore()
const userStore = useUserStore()
const saving = ref(false)
const testing = ref(false)

const form = reactive({
  smtp_host: 'smtp.qq.com',
  smtp_port: 465,
  smtp_user: '',
  smtp_password: '',
  smtp_from_name: '千寻农业助手',
  smtp_from_email: '',
})

const loadConfig = () => {
  const c = configStore.config
  if (!c) return
  form.smtp_host = c.smtp_host || 'smtp.qq.com'
  form.smtp_port = c.smtp_port || 465
  form.smtp_user = c.smtp_user || ''
  form.smtp_password = c.smtp_password || ''
  form.smtp_from_name = c.smtp_from_name || '千寻农业助手'
  form.smtp_from_email = c.smtp_from_email || ''
}

watch(() => configStore.config, loadConfig, { immediate: true })

const handleSave = async () => {
  saving.value = true
  try {
    await configStore.setConfigValues({
      smtp_host: form.smtp_host,
      smtp_port: form.smtp_port,
      smtp_user: form.smtp_user,
      smtp_password: form.smtp_password,
      smtp_from_name: form.smtp_from_name,
      smtp_from_email: form.smtp_from_email,
    })
    message.success('邮件配置已保存')
  } catch (e) {
    message.error('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}

const handleTest = async () => {
  testing.value = true
  try {
    // 先保存当前配置
    await handleSave()
    // 发送测试邮件到当前用户邮箱
    const { apiPost } = await import('@/apis/base')
    const result = await apiPost('/api/email/test', {}, {}, true)
    if (result.code === 0) {
      message.success('测试邮件已发送，请查收')
    } else {
      message.error(result.message || '发送失败')
    }
  } catch (e) {
    message.error('测试失败: ' + e.message)
  } finally {
    testing.value = false
  }
}
</script>

<style lang="less" scoped>
.email-settings-section {
  max-width: 600px;

  .section-title {
    color: var(--gray-900);
    font-size: 16px;
    font-weight: 600;
    margin: 12px 0 4px 0;
  }

  .section-desc {
    color: var(--gray-500);
    font-size: 13px;
    margin: 0 0 20px 0;
  }

  .settings-form {
    display: flex;
    flex-direction: column;
    gap: 16px;

    .form-item {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .form-label {
        font-size: 13px;
        font-weight: 500;
        color: var(--gray-700);
      }

      .form-hint {
        font-size: 12px;
        color: var(--gray-400);
      }
    }

    .form-actions {
      display: flex;
      gap: 12px;
      margin-top: 8px;
    }
  }
}
</style>
