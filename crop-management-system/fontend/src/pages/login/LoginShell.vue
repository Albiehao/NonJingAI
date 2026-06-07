<template>
  <div class="login-shell">
    <video-background />
    <div class="login-shell__content">
      <login-page />
    </div>
  </div>
</template>

<script>
import VideoBackground from '../../components/layout/VideoBackground.vue'
import LoginPage from '../../features/login/LoginPage.vue'

export default {
  name: 'LoginShell',
  components: { VideoBackground, LoginPage }
}
</script>

<style scoped>
.login-shell__content {
  position: relative;
  z-index: 1;
}
</style>
