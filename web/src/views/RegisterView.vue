<template>
  <div class="register-view">
    <div class="register-container">
      <LoginBanner />

      <!-- 右侧注册面板 -->
      <div class="register-panel">
        <div class="panel-inner">
          <div class="panel-nav">
            <a-button type="text" class="back-btn" @click="goLogin">
              <left-outlined /> 返回登录
            </a-button>
          </div>

          <div class="panel-form">
            <div class="form-header">
              <h2 class="form-title">创建账号</h2>
              <p class="form-subtitle">注册后即可开始使用</p>
            </div>

            <div class="form-body">
              <a-form :model="form" @finish="handleRegister" layout="vertical">
                <a-form-item
                  name="username"
                  :rules="[
                    { required: true, message: '请输入用户名' },
                    { min: 2, max: 20, message: '用户名长度2-20个字符' },
                    { pattern: /^[a-zA-Z0-9_一-龥]+$/, message: '用户名包含非法字符' }
                  ]"
                >
                  <a-input v-model:value="form.username" placeholder="用户名" size="large">
                    <template #prefix><user-outlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="email"
                  :rules="[
                    { required: true, message: '请输入邮箱' },
                    { type: 'email', message: '请输入正确的邮箱格式' }
                  ]"
                >
                  <div class="email-row">
                    <a-input v-model:value="form.email" placeholder="邮箱" size="large" class="email-input">
                      <template #prefix><mail-outlined /></template>
                    </a-input>
                    <a-button
                      :disabled="!form.email || codeSending"
                      @click="handleSendCode"
                      :loading="codeSending"
                      size="large"
                      class="code-btn"
                    >
                      {{ codeCountdown > 0 ? `${codeCountdown}s` : '发送验证码' }}
                    </a-button>
                  </div>
                </a-form-item>

                <a-form-item
                  name="email_code"
                  :rules="[{ required: true, message: '请输入验证码' }]"
                >
                  <a-input v-model:value="form.email_code" placeholder="邮箱验证码" :maxlength="6" size="large">
                    <template #prefix><safety-outlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="password"
                  :rules="[
                    { required: true, message: '请输入密码' },
                    { min: 6, message: '密码至少6个字符' }
                  ]"
                >
                  <a-input-password v-model:value="form.password" placeholder="密码（至少6位）" size="large">
                    <template #prefix><lock-outlined /></template>
                  </a-input-password>
                </a-form-item>

                <a-form-item
                  name="confirmPassword"
                  :rules="[
                    { required: true, message: '请确认密码' },
                    { validator: validateConfirm }
                  ]"
                >
                  <a-input-password v-model:value="form.confirmPassword" placeholder="确认密码" size="large">
                    <template #prefix><lock-outlined /></template>
                  </a-input-password>
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit" :loading="loading" block size="large" class="register-btn">
                    注 册
                  </a-button>
                </a-form-item>
              </a-form>

              <div class="form-footer-links">
                <span class="login-hint">
                  已有账号？<a @click="goLogin">立即登录</a>
                </span>
              </div>

              <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
            </div>
          </div>

          <div class="panel-footer">
            &copy; {{ new Date().getFullYear() }} {{ brandName }}. All Rights Reserved.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInfoStore } from '@/stores/info'
import { message } from 'ant-design-vue'
import { sendRegisterCode, registerUser } from '@/apis/register_api'
import {
  UserOutlined,
  LockOutlined,
  MailOutlined,
  SafetyOutlined,
  LeftOutlined
} from '@ant-design/icons-vue'
import LoginBanner from '@/components/LoginBanner.vue'

const router = useRouter()
const infoStore = useInfoStore()

const brandName = computed(() => {
  const orgName = infoStore.organization?.name?.trim() || ''
  const brandNameRaw = infoStore.branding?.name?.trim() || 'QianXun'
  if (orgName && brandNameRaw && orgName !== brandNameRaw) return brandNameRaw
  return orgName || brandNameRaw
})

const form = reactive({
  username: '',
  email: '',
  email_code: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const codeSending = ref(false)
const codeCountdown = ref(0)
let countdownTimer = null
const errorMessage = ref('')

const startCountdown = () => {
  codeCountdown.value = 60
  countdownTimer = setInterval(() => {
    codeCountdown.value--
    if (codeCountdown.value <= 0) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer)
})

const handleSendCode = async () => {
  if (!form.email) {
    message.warning('请先输入邮箱')
    return
  }
  codeSending.value = true
  try {
    await sendRegisterCode(form.email)
    message.success('验证码已发送')
    startCountdown()
  } catch (e) {
    message.error(e.message || '发送失败')
  } finally {
    codeSending.value = false
  }
}

const validateConfirm = async (rule, value) => {
  if (!value) throw new Error('请确认密码')
  if (value !== form.password) throw new Error('两次输入的密码不一致')
}

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    await registerUser({
      username: form.username,
      password: form.password,
      email: form.email,
      email_code: form.email_code
    })
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    errorMessage.value = e.message || '注册失败'
  } finally {
    loading.value = false
  }
}

const goLogin = () => router.push('/login')
</script>

<style lang="less" scoped>
.register-view {
  min-height: 100vh;
  width: 100%;
  background: var(--gray-10);
}

.register-container {
  display: flex;
  height: 100vh;
}

/* ===== 右侧注册面板 ===== */
.register-panel {
  flex: 1;
  min-width: 480px;
  max-width: 50%;
  background: var(--gray-0);
  display: flex;
  flex-direction: column;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px);
    background-size: 24px 24px;
    pointer-events: none;
  }

  @media (max-width: 1024px) {
    width: 100%;
    min-width: 0;
    max-width: none;
  }
}

.panel-inner {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 40px;
  overflow-y: auto;
}

.panel-nav {
  flex-shrink: 0;

  .back-btn {
    color: var(--gray-500);
    font-size: 14px;
    padding: 4px 8px;
    height: auto;

    &:hover {
      color: var(--main-color);
      background: transparent;
    }
  }
}

.panel-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 640px;
  margin: 0 auto;
  width: 100%;
}

.form-header {
  margin-bottom: 40px;

  .form-title {
    font-size: 34px;
    font-weight: 700;
    color: var(--gray-900);
    margin: 0 0 10px;
    line-height: 1.2;
  }

  .form-subtitle {
    font-size: 17px;
    color: var(--gray-500);
    margin: 0;
  }
}

.form-body {
  width: 100%;
}

:deep(.ant-form-item) {
  margin-bottom: 24px;
}

:deep(.ant-input-affix-wrapper) {
  padding: 10px 16px;
  border-radius: 4px;
  border-color: var(--gray-300);

  &:hover,
  &:focus {
    border-color: var(--main-color);
  }

  .anticon {
    color: var(--gray-400);
    font-size: 18px;
  }
}

:deep(.ant-input) {
  font-size: 17px;
}

:deep(.ant-input-password) {
  border-radius: 4px;
  border-color: var(--gray-300);
}

.email-row {
  display: flex;
  gap: 8px;

  .email-input {
    flex: 1;
  }
}

.code-btn {
  flex-shrink: 0;
  border-radius: 4px;
}

.register-btn {
  height: 48px;
  font-size: 17px;
  border-radius: 4px;
  border-color: var(--color-primary-500) !important;
  background-color: var(--color-primary-500) !important;
}

.register-btn:hover {
  border-color: var(--color-primary-700) !important;
  background-color: var(--color-primary-700) !important;
}

.form-footer-links {
  text-align: center;

  .login-hint {
    font-size: 14px;
    color: var(--gray-500);

    a {
      color: var(--main-color);
    }
  }
}

.error-msg {
  margin-top: 16px;
  padding: 10px 12px;
  background: var(--color-error-50);
  border: 1px solid color-mix(in srgb, var(--color-error-500) 25%, transparent);
  border-radius: 4px;
  color: var(--color-error-700);
  font-size: 13px;
  text-align: center;
}

.panel-footer {
  flex-shrink: 0;
  text-align: center;
  font-size: 12px;
  color: var(--gray-400);
  padding-top: 20px;
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .register-panel {
    width: 100%;
    min-width: 0;
  }

  .panel-form {
    max-width: 520px;
  }
}

@media (max-width: 576px) {
  .panel-inner {
    padding: 24px 20px;
  }
}
</style>