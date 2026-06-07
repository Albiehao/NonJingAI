<template>
  <div class="login-page" :class="{ 'light-mode': isLightMode }">
    <button class="back-btn" type="button" aria-label="返回" title="返回" @click="handleBack">
      <span class="back-icon" aria-hidden="true">‹</span>
    </button>
    <div class="login-container">
      <!-- 左侧大图区域 -->
      <div class="left-section">
        <img src="https://cdn.pixabay.com/photo/2023/06/25/11/00/wheat-8087042_1280.jpg" alt="background" class="bg-image" />
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
                    <input v-model="loginForm.password" :type="showLoginPassword ? 'text' : 'password'" class="form-input has-eye" placeholder="请输入密码" />
                    <button class="eye-btn" type="button" :title="showLoginPassword ? '隐藏密码' : '显示密码'" @click="showLoginPassword = !showLoginPassword">
                      <span
                        class="eye-icon"
                        :style="{
                          WebkitMaskImage: `url(${showLoginPassword ? eyeOpenIcon : eyeOffIcon})`,
                          maskImage: `url(${showLoginPassword ? eyeOpenIcon : eyeOffIcon})`
                        }"
                      ></span>
                    </button>
                  </div>
                </div>

                <div class="form-options">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="loginForm.remember" />
                    <span>记住登录状态</span>
                  </label>
                  <a href="#" @click="passwordForget" class="link-text">忘记密码？</a>
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
                    <input v-model="registerForm.password" :type="showRegisterPassword ? 'text' : 'password'" class="form-input has-eye" placeholder="请设置密码" />
                    <button class="eye-btn" type="button" :title="showRegisterPassword ? '隐藏密码' : '显示密码'" @click="showRegisterPassword = !showRegisterPassword">
                      <span
                        class="eye-icon"
                        :style="{
                          WebkitMaskImage: `url(${showRegisterPassword ? eyeOpenIcon : eyeOffIcon})`,
                          maskImage: `url(${showRegisterPassword ? eyeOpenIcon : eyeOffIcon})`
                        }"
                      ></span>
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">确认密码</label>
                  <div class="input-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
                    </svg>
                    <input v-model="registerForm.confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" class="form-input has-eye" placeholder="请再次输入密码" />
                    <button class="eye-btn" type="button" :title="showConfirmPassword ? '隐藏密码' : '显示密码'" @click="showConfirmPassword = !showConfirmPassword">
                      <span
                        class="eye-icon"
                        :style="{
                          WebkitMaskImage: `url(${showConfirmPassword ? eyeOpenIcon : eyeOffIcon})`,
                          maskImage: `url(${showConfirmPassword ? eyeOpenIcon : eyeOffIcon})`
                        }"
                      ></span>
                    </button>
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
import eyeOpenIcon from '../assets/eye-open.svg'
import eyeOffIcon from '../assets/eye-off.svg'
export default {
  components: { HmButton, HmTabSwitch },
  name: 'LoginComponent',
  props: {
    isLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      eyeOpenIcon,
      eyeOffIcon,
      activeTab: 'login',
      showLoginPassword: false,
      showRegisterPassword: false,
      showConfirmPassword: false,
      loginForm: { username: '', password: '', remember: false },
      registerForm: { username: '', phone: '', password: '', confirmPassword: '' }
    }
  },
  methods: {
    handleBack() {
      this.$emit('back')
    },
    handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) return alert('请填写完整信息')
      this.$emit('login', this.loginForm)
    },
    handleRegister() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) return alert('两次密码输入不一致')
      this.$emit('register', this.registerForm)
    },
    passwordForget(){
      alert("暂时未实现！")
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
    rgba(17, 20, 27, 0.55);
  background-size: 8px 8px, auto;
  font-family: 'Courier New', 'Lucida Console', monospace;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 16px;
  left: 20px;
  z-index: 5;
  border: none;
  background: transparent;
  color: rgba(245, 230, 204, 0.82);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 10px;
  line-height: 1;
}

.back-btn:hover {
  color: rgba(255, 232, 176, 0.95);
}

.back-btn:active {
  transform: translateY(1px);
}

.back-icon {
  font-size: 28px;
  line-height: 1;
  font-weight: 700;
  transform: translateX(-1px);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
}

.login-container {
  display: flex;
  width: 1000px;
  height: 640px;
  border-radius: 2px;
  border: none;
  overflow: hidden;
  box-shadow:
    0 0 0 3px #8d6b4b,
    0 16px 0 rgba(0, 0, 0, 0.35);
}

/* 左侧：全页视频透出 */
.left-section {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-height: 0;
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

.form-input.has-eye {
  padding-right: 62px;
}

.eye-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  color: #c8b89a;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  cursor: pointer;
}

.eye-btn:hover {
  color: #ffe8b0;
}

.eye-icon {
  width: 16px;
  height: 16px;
  background-color: currentColor;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
}

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

.login-page.light-mode {
  background:
    linear-gradient(rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.035) 1px, transparent 1px);
  background-size: 10px 10px, 10px 10px;
}

.login-page.light-mode .right-section {
  background: #e8dece;
}

.login-page.light-mode .login-container {
  border: 3px solid #2a1c12;
  box-shadow: none;
}

.login-page.light-mode .left-overlay {
  background: transparent;
}

.login-page.light-mode .form-label {
  color: #4b3a2b;
  text-shadow: none;
}

.login-page.light-mode .form-input {
  background: #f1e9db;
  color: #433224;
  border-color: #8d6b4b;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.login-page.light-mode .form-input:focus {
  background: #ece1d0;
  border-color: #6f4c30;
  box-shadow:
    0 0 0 2px rgba(111, 76, 48, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.login-page.light-mode .input-wrapper:focus-within .input-icon {
  color: #6f4c30;
}

.login-page.light-mode .eye-btn {
  color: #6f4c30;
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

.login-page.light-mode .back-btn {
  background: transparent;
  border: none;
  color: rgba(75, 58, 43, 0.78);
}
</style>