<template>
  <div class="login-page" :class="{ 'light-mode': isLightMode }">
    <button
      class="theme-toggle"
      :class="{ on: isLightMode }"
      type="button"
      :title="isLightMode ? '关灯模式' : '开灯模式'"
      @click="isLightMode = !isLightMode"
    >
      <svg class="theme-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M0 1024h1024V0H0v1024z" fill="none"></path>
        <path d="M42.666667 512h42.666666v213.333333H42.666667zM85.333333 725.333333h85.333334v42.666667H85.333333zM170.666667 725.333333h42.666666v42.666667H170.666667zM85.333333 469.333333h213.333334v42.666667H85.333333zM213.333333 682.666667h42.666667v42.666666H213.333333zM85.333333 554.666667h42.666667v42.666666H85.333333zM256 682.666667h42.666667v42.666666H256zM298.666667 682.666667h85.333333v42.666666H298.666667zM128 597.333333h298.666667v42.666667H128zM341.333333 426.666667h85.333334v42.666666H341.333333zM298.666667 469.333333h42.666666v42.666667H298.666667zM384 682.666667h42.666667v42.666666H384zM426.666667 725.333333h85.333333v42.666667h-85.333333zM469.333333 682.666667h42.666667v42.666666h-42.666667zM469.333333 640h42.666667v42.666667h-42.666667zM512 597.333333h42.666667v42.666667h-42.666667zM597.333333 554.666667h85.333334v42.666666h-85.333334z"></path>
        <path d="M512 597.333333h42.666667v42.666667h-42.666667zM512 554.666667h42.666667v42.666666h-42.666667zM554.666667 554.666667h42.666666v42.666666h-42.666666zM469.333333 597.333333h42.666667v42.666667h-42.666667zM426.666667 426.666667h42.666666v42.666666h-42.666666zM682.666667 554.666667h85.333333v42.666666h-85.333333zM768 554.666667h42.666667v42.666666h-42.666667zM810.666667 554.666667h42.666666v42.666666h-42.666666zM853.333333 554.666667h42.666667v42.666666h-42.666667zM896 597.333333h42.666667v42.666667h-42.666667zM896 554.666667h42.666667v42.666666h-42.666667zM938.666667 597.333333h42.666666v42.666667h-42.666666zM768 426.666667h42.666667v42.666666h-42.666667zM768 384h42.666667v42.666667h-42.666667zM938.666667 640h42.666666v42.666667h-42.666666zM469.333333 256h42.666667v213.333333h-42.666667zM469.333333 213.333333h42.666667v42.666667h-42.666667zM426.666667 170.666667h85.333333v42.666666h-85.333333zM512 213.333333h426.666667v42.666667H512zM768 170.666667h170.666667v42.666666h-170.666667zM512 298.666667h42.666667v256h-42.666667zM853.333333 256h42.666667v298.666667h-42.666667zM597.333333 469.333333h170.666667v42.666667h-170.666667z"></path>
        <path d="M597.333333 640h256v256h-256v-256z m213.333334 42.666667h-170.666667v170.666666h170.666667v-170.666666z"></path>
        <path d="M256 810.666667h42.666667v42.666666H256zM341.333333 810.666667h42.666667v42.666666H341.333333zM256 768h128v42.666667H256zM256 853.333333h128v42.666667H256z"></path>
      </svg>
      <span class="theme-text">{{ isLightMode ? '关灯' : '开灯' }}</span>
    </button>
    <div class="login-container">
      <!-- 左侧大图区域 -->
      <div class="left-section">
        <img src="https://cdn.pixabay.com/photo/2022/05/27/18/09/grain-field-7225738_1280.jpg" alt="background" class="bg-image" />
        <div class="left-overlay">
          <div class="brand-header">
            <h1 class="brand-title">禾信综合农资平台</h1>
            <p class="brand-subtitle">Agricultural Intelligence Platform</p>
          </div>
          <p class="slogan">喜看稻菽千重浪，遍地英雄下夕烟</p>
        </div>
      </div>

      <!-- 右侧表单区 -->
      <div class="right-section">
        <div class="form-wrapper">
          <!-- Tab 切换 -->
          <hm-tab-switch v-model="activeTab" />

          <transition name="slide-fade" mode="out-in">
            <!-- 登录表单 -->
            <form v-if="activeTab === 'login'" key="login" class="form-content" @submit.prevent="handleLogin">
              <div class="form-inner">
                <div class="form-group">
                  <label class="form-label">账号</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
                    </svg>
                    <input v-model="loginForm.username" type="text" class="form-input" placeholder="请输入账号" />
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">密码</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
                    </svg>
                    <input v-model="loginForm.password" type="password" class="form-input" placeholder="请输入密码" />
                  </div>
                </div>

                <div class="form-options">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="loginForm.remember" />
                    <span>记住登录状态</span>
                  </label>
                  <a href="#" class="link-text">忘记密码？</a>
                </div>
              </div>

              <div class="hm-button-wrap">
                <hm-button label="登录"></hm-button>
              </div>
            </form>

            <!-- 注册表单 -->
            <form v-else key="register" class="form-content" @submit.prevent="handleRegister">
              <div class="form-inner">
                <div class="form-group">
                  <label class="form-label">用户名</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
                    </svg>
                    <input v-model="registerForm.username" type="text" class="form-input" placeholder="请输入用户名" />
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">手机号</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>
                    </svg>
                    <input v-model="registerForm.phone" type="tel" class="form-input" placeholder="请输入手机号" />
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">密码</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
                    </svg>
                    <input v-model="registerForm.password" type="password" class="form-input" placeholder="请设置密码" />
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">确认密码</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
                    </svg>
                    <input v-model="registerForm.confirmPassword" type="password" class="form-input" placeholder="请再次输入密码" />
                  </div>
                </div>
              </div>

              <div class="hm-button-wrap">
                <hm-button label="注册"></hm-button>
              </div>
            </form>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HmButton from './common/HmButton.vue'
import HmTabSwitch from './forms/HmTabSwitch.vue'
export default {
  components: { HmButton, HmTabSwitch },
  name: 'LoginComponent',
  data() {
    return {
      isLightMode: false,
      activeTab: 'login',
      loginForm: { username: '', password: '', remember: false },
      registerForm: { username: '', phone: '', password: '', confirmPassword: '' }
    }
  },
  methods: {
    handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) return alert('请填写完整信息')
      this.$emit('login', this.loginForm)
    },
    handleRegister() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) return alert('两次密码输入不一致')
      this.$emit('register', this.registerForm)
    }
  }
}
</script>

<style scoped>
* { margin: 0; padding: 0; box-sizing: border-box; }

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    #11141b;
  background-size: 8px 8px, 8px 8px, auto;
  font-family: 'Courier New', 'Lucida Console', monospace;
  position: relative;
}

.login-container {
  display: flex;
  width: 1000px;
  height: 640px;
  border-radius: 2px;
  border: 3px solid #2a1c12;
  overflow: hidden;
  box-shadow:
    0 0 0 3px #8d6b4b,
    0 16px 0 rgba(0, 0, 0, 0.35);
}

/* 左侧大图 */
.left-section {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  image-rendering: pixelated;
  /* 图片未设置时的占位背景 */
  background: linear-gradient(135deg, #15803d, #166534);
}

.left-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.55) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 48px 44px;
}

.brand-title {
  font-size: 40px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 3px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}

.brand-subtitle {
  font-size: 12px;
  color: rgba(255,255,255,0.75);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 8px;
}

.slogan {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  line-height: 1.8;
  letter-spacing: 1px;
}

/* 右侧表单 */
.right-section {
  width: 460px;
  height: 640px;
  background: #1f252f;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-left: 3px solid #2a1c12;
}

.form-wrapper {
  width: 360px;
  margin: 0 auto;
  transform: translateY(24px);
  height: 500px;
  display: flex;
  flex-direction: column;
}

.form-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.form-inner {
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
  justify-content: center;
  transform: translateY(-10px);
}

.hm-button-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: auto;
  padding-top: 12px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-label {
  font-size: 12px;
  font-weight: bold;
  color: #f5e6cc;
  letter-spacing: 1px;
  text-shadow: 0 1px 0 rgba(0, 0, 0, 0.65);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  width: 18px;
  height: 18px;
  color: #c8b89a;
  pointer-events: none;
  transition: color 0.3s;
}

.input-wrapper:focus-within .input-icon { color: #ffe8b0; }

.form-input {
  width: 100%;
  padding: 13px 14px 13px 44px;
  border: 2px solid #2a1c12;
  border-radius: 1px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #f5e6cc;
  background: #2b3038;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.form-input:focus {
  border-color: #8d6b4b;
  background: #333a45;
  box-shadow:
    0 0 0 2px rgba(141, 107, 75, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.form-input::placeholder { color: #8e98a8; }

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  color: #d2c3a5;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 15px;
  height: 15px;
  accent-color: #8d6b4b;
  cursor: pointer;
}

.link-text {
  font-size: 12px;
  color: #f1c98b;
  text-decoration: none;
  font-weight: bold;
  letter-spacing: 1px;
}

.slide-fade-enter-active,
.slide-fade-leave-active { transition: all 0.25s ease; }
.slide-fade-enter { opacity: 0; transform: translateX(16px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-16px); }

.theme-toggle {
  position: absolute;
  top: 16px;
  right: 20px;
  min-width: 86px;
  height: 34px;
  border: none;
  background: transparent;
  color: #f5e6cc;
  padding: 0;
  border-radius: 0;
  cursor: pointer;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  image-rendering: pixelated;
}

.theme-icon {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.theme-text {
  font-size: 12px;
  font-weight: bold;
  letter-spacing: 1px;
  font-family: 'Courier New', monospace;
}

.theme-toggle.on {
  color: #ffd86b;
  box-shadow: none;
}

.login-page.light-mode {
  background:
    linear-gradient(rgba(0, 0, 0, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.02) 1px, transparent 1px),
    #f8f6f1;
  background-size: 8px 8px, 8px 8px, auto;
}

.login-page.light-mode .right-section {
  background: #fdfaf3;
  border-left-color: #bba07f;
}

.login-page.light-mode .login-container {
  border-color: #bba07f;
  box-shadow: none;
}

.login-page.light-mode .left-overlay {
  background: linear-gradient(to bottom, rgba(255,255,255,0.08) 0%, rgba(0,0,0,0.28) 100%);
}

.login-page.light-mode .form-label {
  color: #4b3a2b;
  text-shadow: none;
}

.login-page.light-mode .form-input {
  background: #ffffff;
  color: #433224;
  border-color: #8d6b4b;
  box-shadow: none;
}

.login-page.light-mode .form-input:focus {
  background: #ffffff;
  border-color: #6f4c30;
  box-shadow: none;
}

.login-page.light-mode .form-input::placeholder {
  color: #8a7a68;
}

.login-page.light-mode .checkbox-label {
  color: #5a4634;
}

.login-page.light-mode .link-text {
  color: #6f4c30;
}

.login-page.light-mode .theme-toggle {
  color: #6f4c30;
}

.login-page.light-mode .theme-toggle.on {
  color: #b27a24;
}
</style>