<template>
  <login-page :is-light-mode="globalLightMode" @login="handleLogin" @register="handleRegister" @back="goHome" />
</template>

<script>
import LoginPage from '../features/login/LoginPage.vue'
import { login, register } from '@/api/user'

export default {
  name: 'LoginView',
  components: { LoginPage },
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    async handleLogin(formData) {
      try {
        const res = await login(formData.username, formData.password)
        if (res.code === 0) {
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('username', res.data.username)
          localStorage.setItem('role', res.data.role)
          localStorage.setItem('userId', res.data.id)
          if (res.data.avatar) localStorage.setItem('avatar', res.data.avatar)
          this.$toast.success('登录成功')
          this.$router.push('/')
        } else {
          this.$toast.error(res.message || '登录失败')
        }
      } catch (e) {
        this.$toast.error('登录失败，请检查网络或账号密码')
      }
    },
    async handleRegister(formData) {
      try {
        const res = await register(formData.username, formData.password, formData.phone)
        if (res.code === 0) {
          this.$toast.success('注册成功，请登录')
        } else {
          this.$toast.error(res.message || '注册失败')
        }
      } catch (e) {
        this.$toast.error('注册失败，请检查网络')
      }
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>