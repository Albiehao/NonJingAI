<template>
  <div class="login-view" :class="{ 'has-alert': serverStatus === 'error' }">
    <!-- 服务状态提示 -->
    <div v-if="serverStatus === 'error'" class="server-status-alert">
      <div class="alert-content">
        <exclamation-circle-outlined class="alert-icon" />
        <div class="alert-text">
          <div class="alert-title">服务端连接失败</div>
          <div class="alert-message">{{ serverError }}</div>
        </div>
        <a-button type="link" size="small" @click="checkServerHealth" :loading="healthChecking">
          重试
        </a-button>
      </div>
    </div>

    <div class="login-container">
      <LoginBanner />

      <!-- 右侧登录 -->
      <div class="login-panel">
        <div class="panel-inner">
          <!-- 返回首页 -->
          <div class="panel-nav">
            <a-button type="text" class="back-btn" @click="goHome">
              <left-outlined /> 返回首页
            </a-button>
          </div>

          <!-- 表单区域 -->
          <div class="panel-form">
            <div class="form-header">
              <h2 class="form-title">欢迎登录</h2>
              <p class="form-subtitle">请使用您的账号登录系统</p>
              <p v-if="isFirstRun" class="init-hint">系统初始化，请创建超级管理员</p>
            </div>

            <!-- 初始化管理员表单 -->
            <div v-if="isFirstRun" class="form-body">
              <a-form :model="adminForm" @finish="handleInitialize" layout="vertical">
                <a-form-item
                  label="用户ID"
                  name="user_id"
                  :rules="[
                    { required: true, message: '请输入用户ID' },
                    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户ID只能包含字母、数字和下划线' },
                    { min: 3, max: 20, message: '用户ID长度必须在3-20个字符之间' }
                  ]"
                >
                  <a-input v-model:value="adminForm.user_id" placeholder="请输入用户ID（3-20个字符）" :maxlength="20" />
                </a-form-item>

                <a-form-item
                  label="邮箱（用于接收通知）"
                  name="email"
                  :rules="[{ type: 'email', message: '请输入正确的邮箱格式' }]"
                >
                  <a-input v-model:value="adminForm.email" placeholder="超级管理员邮箱，可不填" />
                </a-form-item>

                <a-form-item label="密码" name="password" :rules="[{ required: true, message: '请输入密码' }]">
                  <a-input-password v-model:value="adminForm.password" />
                </a-form-item>

                <a-form-item
                  label="确认密码"
                  name="confirmPassword"
                  :rules="[
                    { required: true, message: '请确认密码' },
                    { validator: validateConfirmPassword }
                  ]"
                >
                  <a-input-password v-model:value="adminForm.confirmPassword" />
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit" :loading="loading" block size="large">
                    创建管理员账户
                  </a-button>
                </a-form-item>
              </a-form>
            </div>

            <!-- 登录表单 -->
            <div v-else class="form-body">
              <a-form :model="loginForm" @finish="handleLogin" layout="vertical">
                <a-form-item
                  name="loginId"
                  :rules="[
                    { required: true, message: '请输入邮箱或用户名' }
                  ]"
                >
                  <a-input v-model:value="loginForm.loginId" placeholder="邮箱或用户名" size="large">
                    <template #prefix><user-outlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item name="password" :rules="[{ required: true, message: '请输入密码' }]">
                  <a-input-password v-model:value="loginForm.password" placeholder="密码" size="large">
                    <template #prefix><lock-outlined /></template>
                  </a-input-password>
                </a-form-item>

                <a-form-item>
                  <div class="form-options">
                    <a-checkbox v-model:checked="rememberMe" @click="showDevMessage">记住我</a-checkbox>
                    <a class="forgot-link" @click="showDevMessage">忘记密码?</a>
                  </div>
                </a-form-item>

                <a-form-item>
                  <a-button
                    type="primary"
                    html-type="submit"
                    :loading="loading"
                    :disabled="isLocked"
                    block
                    size="large"
                    class="login-btn"
                  >
                    <span v-if="isLocked">账户已锁定 {{ formatTime(lockRemainingTime) }}</span>
                    <span v-else>登 录</span>
                  </a-button>
                </a-form-item>

                <div class="form-footer-links">
                  <span class="register-hint">
                    还没有账号？<a @click="goRegister">立即注册</a>
                  </span>
                </div>

              </a-form>

              <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
            </div>
          </div>

          <!-- 版权 -->
          <div class="panel-footer">
            &copy; {{ new Date().getFullYear() }} {{ brandName }}. All Rights Reserved.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useInfoStore } from '@/stores/info'
import { useAgentStore } from '@/stores/agent'
import { message } from 'ant-design-vue'
import { healthApi } from '@/apis/system_api'
import {
  UserOutlined,
  LockOutlined,
  ExclamationCircleOutlined,
  LeftOutlined
} from '@ant-design/icons-vue'
import LoginBanner from '@/components/LoginBanner.vue'

const router = useRouter()
const userStore = useUserStore()
const infoStore = useInfoStore()
const agentStore = useAgentStore()

const brandName = computed(() => {
  const orgName = infoStore.organization?.name?.trim() || ''
  const brandNameRaw = infoStore.branding?.name?.trim() || 'QianXun'
  if (orgName && brandNameRaw && orgName !== brandNameRaw) return brandNameRaw
  return orgName || brandNameRaw
})

// 状态
const isFirstRun = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const rememberMe = ref(false)
const serverStatus = ref('loading')
const serverError = ref('')
const healthChecking = ref(false)

// 登录锁定
const isLocked = ref(false)
const lockRemainingTime = ref(0)
const lockCountdown = ref(null)

// 登录表单
const loginForm = reactive({
  loginId: '',
  password: ''
})

// 管理员初始化表单
const adminForm = reactive({
  user_id: '',
  password: '',
  confirmPassword: '',
  email: ''
})

const showDevMessage = () => {
  message.info('该功能正在开发中，敬请期待！')
}

const goHome = () => {
  router.push('/')
}

const goRegister = () => {
  router.push('/register')
}

const clearLockCountdown = () => {
  if (lockCountdown.value) {
    clearInterval(lockCountdown.value)
    lockCountdown.value = null
  }
}

const startLockCountdown = (remainingSeconds) => {
  clearLockCountdown()
  isLocked.value = true
  lockRemainingTime.value = remainingSeconds
  lockCountdown.value = setInterval(() => {
    lockRemainingTime.value--
    if (lockRemainingTime.value <= 0) {
      clearLockCountdown()
      isLocked.value = false
      errorMessage.value = ''
    }
  }, 1000)
}

const formatTime = (seconds) => {
  if (seconds < 60) return `${seconds}秒`
  if (seconds < 3600) {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m}分${s}秒`
  }
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  return `${h}小时${m}分钟`
}

const validateConfirmPassword = async (rule, value) => {
  if (value === '') throw new Error('请确认密码')
  if (value !== adminForm.password) throw new Error('两次输入的密码不一致')
}

const handleLogin = async () => {
  if (isLocked.value) {
    message.warning(`账户被锁定，请等待 ${formatTime(lockRemainingTime.value)}`)
    return
  }
  try {
    loading.value = true
    errorMessage.value = ''
    clearLockCountdown()
    await userStore.login({ loginId: loginForm.loginId, password: loginForm.password })
    message.success('登录成功')
    const redirectPath = sessionStorage.getItem('redirect') || '/'
    sessionStorage.removeItem('redirect')
    if (redirectPath === '/') {
      if (userStore.isAdmin) {
        router.push('/agent')
        return
      }
      try {
        await agentStore.initialize()
        if (agentStore.defaultAgentId) {
          router.push(`/agent/${agentStore.defaultAgentId}`)
          return
        }
        const agentIds = Object.keys(agentStore.agents)
        if (agentIds.length > 0) {
          router.push(`/agent/${agentIds[0]}`)
          return
        }
        router.push('/')
      } catch (e) {
        console.error('获取智能体信息失败:', e)
        router.push('/')
      }
    } else {
      router.push(redirectPath)
    }
  } catch (error) {
    console.error('登录失败:', error)
    if (error.status === 423) {
      let remainingTime = 0
      if (error.headers && error.headers.get) {
        const h = error.headers.get('X-Lock-Remaining')
        if (h) remainingTime = parseInt(h)
      }
      if (remainingTime === 0) {
        const m = error.message.match(/(\d+)\s*秒/)
        if (m) remainingTime = parseInt(m[1])
      }
      if (remainingTime > 0) {
        startLockCountdown(remainingTime)
        errorMessage.value = `由于多次登录失败，账户已被锁定 ${formatTime(remainingTime)}`
      } else {
        errorMessage.value = error.message || '账户被锁定，请稍后再试'
      }
    } else {
      errorMessage.value = error.message || '登录失败，请检查用户名和密码'
    }
  } finally {
    loading.value = false
  }
}

const handleInitialize = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    if (adminForm.password !== adminForm.confirmPassword) {
      errorMessage.value = '两次输入的密码不一致'
      return
    }
    await userStore.initialize({
      user_id: adminForm.user_id,
      password: adminForm.password,
      email: adminForm.email || null
    })
    message.success('管理员账户创建成功')
    router.push('/')
  } catch (error) {
    console.error('初始化失败:', error)
    errorMessage.value = error.message || '初始化失败，请重试'
  } finally {
    loading.value = false
  }
}

const checkFirstRunStatus = async () => {
  try {
    loading.value = true
    isFirstRun.value = await userStore.checkFirstRun()
  } catch (error) {
    console.error('检查首次运行状态失败:', error)
    errorMessage.value = '系统出错，请稍后重试'
  } finally {
    loading.value = false
  }
}

const checkServerHealth = async () => {
  try {
    healthChecking.value = true
    const response = await healthApi.checkHealth()
    if (response.status === 'ok') {
      serverStatus.value = 'ok'
    } else {
      serverStatus.value = 'error'
      serverError.value = response.message || '服务端状态异常'
    }
  } catch (error) {
    console.error('检查服务器健康状态失败:', error)
    serverStatus.value = 'error'
    serverError.value = error.message || '无法连接到服务端，请检查网络连接'
  } finally {
    healthChecking.value = false
  }
}

onMounted(async () => {
  if (userStore.isLoggedIn) {
    router.push('/')
    return
  }
  await checkServerHealth()
  await checkFirstRunStatus()
})

onUnmounted(() => {
  clearLockCountdown()
})
</script>

<style lang="less" scoped>
.login-view {
  min-height: 100vh;
  width: 100%;
  background: var(--gray-10);

  &.has-alert {
    .login-container {
      height: calc(100vh - 60px);
    }
  }
}

.login-container {
  display: flex;
  height: 100vh;
}

/* ===== 右侧登录面板 ===== */
.login-panel {
  flex: 1;
  min-width: 560px;
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

  .init-hint {
    margin: 14px 0 0;
    font-size: 16px;
    color: var(--main-color);
    font-weight: 500;
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;

  .forgot-link {
    color: var(--main-color);
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
  }
}

.login-btn {
  height: 48px;
  font-size: 17px;
  border-radius: 4px;
  border-color: var(--color-primary-500) !important;
  background-color: var(--color-primary-500) !important;
}

.login-btn:hover {
  border-color: var(--color-primary-700) !important;
  background-color: var(--color-primary-700) !important;
}

.form-footer-links {
  text-align: center;

  .register-hint {
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

/* ===== 服务端错误提示 ===== */
.server-status-alert {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 12px 20px;
  background: var(--color-error-500);
  color: var(--gray-0);
  z-index: 1000;

  .alert-content {
    display: flex;
    align-items: center;
    max-width: 1500px;
    margin: 0 auto;

    .alert-icon {
      font-size: 20px;
      margin-right: 12px;
      color: var(--gray-0);
    }

    .alert-text {
      flex: 1;

      .alert-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 2px;
      }

      .alert-message {
        font-size: 14px;
        opacity: 0.9;
      }
    }

    :deep(.ant-btn-link) {
      color: var(--gray-0);
      border-color: var(--gray-0);

      &:hover {
        color: var(--gray-0);
        background-color: color-mix(in srgb, var(--gray-0) 10%, transparent);
      }
    }
  }
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .login-panel {
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