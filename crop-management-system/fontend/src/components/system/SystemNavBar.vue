<template>
  <nav class="site-header" :class="{ 'light-mode': isLightMode }" aria-label="系统导航栏">
    <div class="brand">
      <img class="brand-logo" src="/img/logo.png" alt="禾信综合农资平台" />
      <div class="brand-text">
        <p class="brand-cn">禾信综合农资平台</p>
        <p class="brand-en">Agricultural Intelligence Platform</p>
      </div>
    </div>

    <div class="nav-actions">
      <button type="button" class="nav-btn" :class="{ active: $route.path === '/' }" @click="$router.push('/')">首页</button>
      <button type="button" class="nav-btn" :class="{ active: $route.path === '/login' }" @click="$router.push('/login')">登录</button>
      <button type="button" class="nav-btn" :class="{ active: $route.path === '/admin' }" @click="$router.push('/admin')">后台</button>
    </div>

    <p class="user-tag">{{ title }} · {{ username }}</p>
  </nav>
</template>

<script>
export default {
  name: 'SystemNavBar',
  props: {
    title: {
      type: String,
      default: '后台管理'
    },
    username: {
      type: String,
      default: 'Admin'
    },
    isLightMode: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.site-header {
  height: 76px;
  border: 2px solid #3f2f1f;
  background: rgba(20, 24, 34, 0.95);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 6px 0 rgba(0, 0, 0, 0.32);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 42px;
  height: 42px;
  border: 2px solid #3f2f1f;
  object-fit: cover;
  display: block;
  image-rendering: pixelated;
  background: #0f1219;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 4px 0 rgba(0, 0, 0, 0.28);
}

.brand-cn {
  font-size: 20px;
  letter-spacing: 1px;
  font-weight: 700;
  color: #ffe5a8;
  text-shadow: 2px 2px 0 #2a1b10;
}

.brand-en {
  margin-top: 4px;
  font-size: 11px;
  color: #b8a98f;
  letter-spacing: 1px;
}

.nav-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
  margin-right: 14px;
}

.nav-btn {
  border: 2px solid #6c4d26;
  background: #2f384a;
  color: #ffe5a8;
  box-shadow: 0 3px 0 #1b2230;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 12px;
}

.nav-btn.active {
  color: #ffd46a;
}

.user-tag {
  color: #d8b77a;
  font-size: 12px;
}

.site-header.light-mode {
  border-color: #9a7348;
  background: rgba(252, 246, 235, 0.9);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.72), 0 6px 0 rgba(135, 100, 62, 0.18);
}

.site-header.light-mode .brand-logo {
  border-color: rgba(154, 115, 72, 0.85);
  background: #f8f0e2;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.62), 0 4px 0 rgba(138, 100, 64, 0.12);
}

.site-header.light-mode .brand-cn {
  color: #5f3c1e;
  text-shadow: 2px 2px 0 rgba(255, 240, 214, 0.75);
}

.site-header.light-mode .brand-en,
.site-header.light-mode .user-tag {
  color: #6a4a2a;
}

.site-header.light-mode .nav-btn {
  border-color: #8c6846;
  background: #dac5a7;
  color: #5f3c1e;
  box-shadow: 0 3px 0 #b09471;
}
</style>
