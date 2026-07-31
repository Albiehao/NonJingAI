<template>
  <div class="App" :class="{ 'light-mode': isLightMode }">
    <video-background />
    <div class="App-content" :class="{ 'with-global-nav': showGlobalNav }">
      <global-nav v-if="showGlobalNav" :is-light-mode="isLightMode" />
      <router-view :global-light-mode="isLightMode" />
    </div>
    <toast-message ref="toast" />

    <div v-if="showGlobalNav" class="floating-actions">
      <button
        v-show="showBackToTop"
        class="utility-fab"
        type="button"
        title="返回页首"
        aria-label="返回页首"
        @click="scrollToTop"
      >
        <span class="utility-fab-text">TOP</span>
      </button>
      <chat-bot :is-light-mode="isLightMode" />
      <button
        class="utility-fab theme-fab"
        :class="{ on: isLightMode }"
        type="button"
        :title="isLightMode ? '关闭灯光模式' : '打开灯光模式'"
        aria-label="全局切换灯光模式"
        @click="toggleTheme"
      >
        <span
          class="theme-icon"
          :style="{ WebkitMaskImage: `url(${lightbulbIcon})`, maskImage: `url(${lightbulbIcon})` }"
          aria-hidden="true"
        ></span>
      </button>
    </div>
  </div>
</template>

<script>
import VideoBackground from './components/layout/VideoBackground.vue'
import GlobalNav from './components/system/GlobalNav.vue'
import ToastMessage from './components/common/ToastMessage.vue'
import ChatBot from './components/ChatBot.vue'
import ToastService from './utils/toast'
import lightbulbIcon from './assets/lightbulb-pixel.svg'

export default {
  name: 'App',
  components: {
    VideoBackground,
    GlobalNav,
    ToastMessage,
    ChatBot
  },
  data() {
    return {
      isLightMode: false,
      lightbulbIcon,
      showBackToTop: false
    }
  },
  created() {
    this.isLightMode = localStorage.getItem('globalLightMode') === '1'
  },
  mounted() {
    ToastService.init(this.$refs.toast)
    window.addEventListener('scroll', this.handleScroll, { passive: true })
    this.handleScroll()
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    toggleTheme() {
      this.isLightMode = !this.isLightMode
      localStorage.setItem('globalLightMode', this.isLightMode ? '1' : '0')
    },
    handleScroll() {
      this.showBackToTop = window.scrollY > 320
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  },
  computed: {
    showGlobalNav() {
      return this.$route.path !== '/login'
    }
  }
}
</script>

<style lang="less">
.App {
  position: relative;
  width: 100%;
  min-height: 100vh;
}

.App-content {
  position: relative;
  z-index: 1;
}

.App-content.with-global-nav {
  padding-top: 60px;
}

.floating-actions {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 30;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.utility-fab {
  width: 50px;
  height: 50px;
  border: 2px solid #4f3a24;
  background: #2f384a;
  color: #f5e6cc;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  border-radius: 0;
  box-shadow: 0 4px 0 #1b2230;
  outline: none;
  image-rendering: pixelated;
  display: flex;
  align-items: center;
  justify-content: center;
}

.App.light-mode .utility-fab {
  border-color: #9a7348;
  background: #efe3d1;
  color: #5c4330;
  box-shadow: 0 4px 0 rgba(125, 88, 48, 0.45);
}

.utility-fab:hover {
  filter: brightness(1.08);
}

.utility-fab:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #1b2230;
}

.App.light-mode .utility-fab:active {
  box-shadow: 0 2px 0 rgba(125, 88, 48, 0.45);
}

.theme-fab.on {
  color: #ffd86b;
  border-color: #816034;
}

.App.light-mode .theme-fab.on {
  color: #9d621f;
  border-color: #9a7348;
}

.utility-fab-text {
  display: block;
  min-width: 22px;
  text-align: center;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
}

.theme-icon {
  width: 22px;
  height: 22px;
  display: block;
  background-color: currentColor;
  filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.65));
}

@media (max-width: 768px) {
  .floating-actions {
    right: 12px;
    bottom: 12px;
    gap: 10px;
  }
}
</style>
