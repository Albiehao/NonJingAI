<template>
  <header class="site-header" :class="{ 'light-mode': isLightMode }">
    <div class="brand" @click="$router.push('/')" title="返回首页">
      <img class="brand-logo" src="/img/logo.png" alt="禾信综合农资平台" />
      <div class="brand-text">
        <p class="brand-cn">禾信综合农资平台</p>
        <p class="brand-en">HEXIN INTEGRATED AGRICULTURAL SUPPLIES PLATFORM</p>
      </div>
    </div>

    <button
      class="menu-toggle"
      type="button"
      :aria-expanded="String(mobileMenuOpen)"
      aria-label="切换导航菜单"
      @click="mobileMenuOpen = !mobileMenuOpen"
    >
      ☰
    </button>

    <nav class="main-nav" :class="{ open: mobileMenuOpen }" aria-label="主导航">
      <a :class="{ active: $route.path === '/' }" @click.prevent="$router.push('/')">主页</a>
      <a :class="{ active: $route.path === '/products' }" @click.prevent="$router.push('/products')">商品中心</a>
      <a :class="{ active: $route.path === '/story' }" @click.prevent="$router.push('/story')">品牌故事</a>
      <a v-if="isAdmin" :class="{ active: $route.path === '/admin' }" @click.prevent="$router.push('/admin')">后台管理</a>
    </nav>

    <div class="right-btn">
      <HmButton v-if="!isLoggedIn" label="登录" type="button" size="nav" @click="goLogin" />
      <div v-else class="user-menu">
        <button
          class="avatar-btn"
          type="button"
          :title="username"
          :aria-expanded="String(userMenuOpen)"
          aria-haspopup="menu"
          @click.stop="toggleUserMenu"
        >
          <img v-if="avatarUrl" :src="avatarUrl" class="avatar-img" alt="头像" />
          <span v-else class="avatar-text">{{ avatarText }}</span>
        </button>
        <div v-if="userMenuOpen" class="user-dropdown" role="menu" aria-label="用户菜单">
          <button type="button" class="user-dropdown-item" role="menuitem" @click="goUserCenter">用户中心</button>
          <button
            v-if="isAdmin"
            type="button"
            class="user-dropdown-item"
            role="menuitem"
            @click="goAdmin"
          >
            后台管理
          </button>
          <button type="button" class="user-dropdown-item danger" role="menuitem" @click="logout">注销</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import HmButton from '../common/HmButton.vue'

export default {
  name: 'GlobalNav',
  components: {
    HmButton
  },
  props: {
    isLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      mobileMenuOpen: false,
      username: '',
      userMenuOpen: false,
      role: '',
      avatar: ''
    }
  },
  created() {
    this.syncUser()
  },
  mounted() {
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleOutsideClick)
  },
  watch: {
    '$route.path'() {
      this.mobileMenuOpen = false
      this.userMenuOpen = false
      this.syncUser()
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.username
    },
    isAdmin() {
      return this.role === 'ADMIN'
    },
    avatarText() {
      return this.username ? this.username.slice(0, 1).toUpperCase() : 'U'
    },
    avatarUrl() {
      if (!this.avatar) return ''
      if (this.avatar.startsWith('http')) return this.avatar
      return 'http://localhost:8080' + this.avatar
    }
  },
  methods: {
    syncUser() {
      this.username = (localStorage.getItem('username') || '').trim()
      this.role = (localStorage.getItem('role') || '').trim()
      this.avatar = (localStorage.getItem('avatar') || '').trim()
    },
    goHome() {
      if (this.$route.path !== '/') {
        this.$router.push('/')
      }
    },
    toggleUserMenu() {
      this.userMenuOpen = !this.userMenuOpen
    },
    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.userMenuOpen = false
      }
    },
    goUserCenter() {
      this.userMenuOpen = false
      if (this.$route.path !== '/user-center') {
        this.$router.push('/user-center')
      }
    },
    goAdmin() {
      this.userMenuOpen = false
      if (this.$route.path !== '/admin') {
        this.$router.push('/admin')
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      localStorage.removeItem('userId')
      localStorage.removeItem('avatar')
      this.userMenuOpen = false
      this.syncUser()
      this.goLogin()
    },
    goLogin() {
      if (this.$route.path !== '/login') {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.site-header {
  --ui-pixel: 'Press Start 2P', 'VT323', 'Pixelify Sans', 'Courier New', monospace;
  --nav-text: #f2e2bf;
  --nav-text-active: #ffffff;
  --nav-mobile-panel-bg: #f4f4f4;
  --nav-mobile-text: #1f2a44;
  --nav-mobile-active: #0d3ea9;
  --nav-mobile-active-bg: #e9efff;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  min-height: 60px;
  border: 2px solid #3f2f1f;
  border-top: none;
  background: rgba(20, 24, 34, 0.95);
  display: flex;
  align-items: center;
  padding: 0 18px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 6px 0 rgba(0, 0, 0, 0.32);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 0 1 300px;
  cursor: pointer;
  z-index: 1;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-logo {
  width: 34px;
  height: 34px;
  border: 2px solid #3f2f1f;
  object-fit: cover;
  display: block;
  image-rendering: pixelated;
  background: #0f1219;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 4px 0 rgba(0, 0, 0, 0.28);
}

.brand-cn {
  font-size: 14px;
  letter-spacing: 0.5px;
  font-weight: 700;
  font-family: var(--ui-pixel);
  color: #f6e5bf;
  text-shadow: 1px 1px 0 #2a1b10;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand-en {
  margin-top: 2px;
  font-size: 9px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  font-family: var(--ui-pixel);
  color: #c6b79f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.main-nav {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(18px, 2.8vw, 42px);
  max-width: min(62vw, 980px);
  overflow: hidden;
}

.main-nav a {
  color: var(--nav-text);
  font-size: 14px;
  font-family: var(--ui-pixel);
  font-weight: 600;
  letter-spacing: 0.3px;
  text-decoration: none;
  cursor: pointer;
  padding: 4px 0;
  white-space: nowrap;
  transition: color 0.2s ease;
}

.main-nav a:hover,
.main-nav a.active {
  color: var(--nav-text-active);
}

.menu-toggle {
  display: none;
  margin-left: auto;
  margin-right: 8px;
  width: 34px;
  height: 34px;
  border: 1px solid #7f6949;
  border-radius: 8px;
  background: linear-gradient(180deg, #8f7656 0%, #5c472f 100%);
  color: #efe0c4;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
}

.right-btn {
  margin-left: auto;
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
}

.avatar-btn {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 0;
}

.avatar-img {
  width: 34px;
  height: 34px;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-text {
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  font-family: var(--ui-pixel);
  color: #f6e5bf;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 132px;
  border: 2px solid #7f6949;
  background: rgba(27, 33, 46, 0.98);
  box-shadow: 0 6px 0 rgba(0, 0, 0, 0.35);
  z-index: 50;
  padding: 4px;
}

.user-dropdown-item {
  width: 100%;
  border: none;
  background: transparent;
  color: #f6e5bf;
  text-align: left;
  font-family: var(--ui-pixel);
  font-size: 12px;
  padding: 8px 10px;
  cursor: pointer;
}

.user-dropdown-item:hover {
  background: rgba(255, 212, 106, 0.14);
}

.user-dropdown-item.danger {
  color: #ffb0a4;
}

.site-header.light-mode {
  background: rgba(252, 246, 235, 0.9);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.72), 0 6px 0 rgba(135, 100, 62, 0.18);
  border-color: #9a7348;
}

.site-header.light-mode .brand-logo {
  border-color: rgba(154, 115, 72, 0.85);
  background: #f8f0e2;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.62), 0 4px 0 rgba(138, 100, 64, 0.12);
}

.site-header.light-mode .brand-cn {
  color: #694322;
  text-shadow: 1px 1px 0 rgba(255, 240, 214, 0.75);
}

.site-header.light-mode .brand-en {
  color: #6a4a2a;
}

.site-header.light-mode .main-nav a {
  color: #694322;
}

.site-header.light-mode .main-nav a:hover,
.site-header.light-mode .main-nav a.active {
  color: #694322;
}

.site-header.light-mode .right-btn {
  filter: brightness(1.03);
}

.site-header.light-mode .avatar-btn {
  border: none;
  background: transparent;
}

.site-header.light-mode .avatar-text {
  color: #5f3c1e;
}

.site-header.light-mode .user-dropdown {
  border-color: #8c6846;
  background: rgba(248, 240, 226, 0.98);
  box-shadow: 0 6px 0 rgba(138, 100, 64, 0.22);
}

.site-header.light-mode .user-dropdown-item {
  color: #5f3c1e;
}

.site-header.light-mode .user-dropdown-item:hover {
  background: rgba(157, 98, 31, 0.12);
}

.site-header.light-mode .user-dropdown-item.danger {
  color: #8e3f31;
}

@media (max-width: 1200px) {
  .main-nav {
    gap: 14px;
    max-width: 56vw;
  }
}

@media (max-width: 980px) {
  .site-header {
    padding: 0 12px;
  }

  .brand {
    flex: 1 1 auto;
    max-width: calc(100% - 150px);
  }

  .brand-en {
    display: block;
    font-size: 7px;
    letter-spacing: 0.5px;
    opacity: 0.9;
  }

  .menu-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    margin-right: 0;
    border: none;
    border-radius: 0;
    background: transparent;
    box-shadow: none;
    color: #694322;
    font-size: 30px;
    font-weight: 600;
    padding: 0;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }

  .right-btn {
    display: none;
  }

  .main-nav {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    transform: none;
    z-index: 20;
    display: none;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    gap: 0;
    max-width: none;
    padding: 0;
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 0;
    background: var(--nav-mobile-panel-bg);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28);
  }

  .main-nav.open {
    display: flex;
  }

  .main-nav a {
    color: var(--nav-mobile-text);
    font-size: 24px;
    font-family: var(--ui-pixel);
    font-weight: 600;
    letter-spacing: 0.6px;
    line-height: 1.35;
    padding: 26px 28px;
    border-bottom: 1px solid #e6e6e6;
  }

  .main-nav a:hover,
  .main-nav a.active {
    color: var(--nav-mobile-active);
    background: var(--nav-mobile-active-bg);
  }
}

@media (max-width: 680px) {
  .brand-logo {
    width: 28px;
    height: 28px;
  }

  .brand-cn {
    font-size: 12px;
  }

  .main-nav a {
    font-size: 21px;
    padding: 20px 18px;
  }
}
</style>
