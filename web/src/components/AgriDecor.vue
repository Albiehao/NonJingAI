<template>
  <div class="agri-scene" :class="`agri-scene--${variant}`" aria-hidden="true">
    <!-- 天空 -->
    <div class="layer-sky"></div>
    <div class="layer-sun"></div>

    <!-- 云彩 -->
    <div class="layer-clouds">
      <div class="cloud cloud-1"></div>
      <div class="cloud cloud-2"></div>
      <div class="cloud cloud-3"></div>
      <div class="cloud cloud-4"></div>
      <div class="cloud cloud-5"></div>
    </div>

    <!-- 飞鸟（固定尺寸，避免撑满屏） -->
    <svg class="bird bird-1" width="28" height="14" viewBox="0 0 28 14">
      <path
        d="M3 9c4-6 8-6 12 0 2-4 4-4 8 0 1.5-2 3-2 5 0"
        fill="none"
        stroke="#5a8268"
        stroke-width="1.3"
        stroke-linecap="round"
      />
    </svg>
    <svg class="bird bird-2" width="22" height="12" viewBox="0 0 28 14">
      <path
        d="M3 9c4-6 8-6 12 0 2-4 4-4 8 0 1.5-2 3-2 5 0"
        fill="none"
        stroke="#6b9478"
        stroke-width="1.2"
        stroke-linecap="round"
      />
    </svg>
    <svg v-if="variant === 'home'" class="bird bird-3" width="20" height="10" viewBox="0 0 28 14">
      <path
        d="M3 9c4-6 8-6 12 0 2-4 4-4 8 0"
        fill="none"
        stroke="#5a8268"
        stroke-width="1.1"
        stroke-linecap="round"
        opacity="0.8"
      />
    </svg>

    <!-- 远景 + 田园底层 -->
    <svg
      class="layer-landscape"
      viewBox="0 0 1440 200"
      preserveAspectRatio="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <!-- 远山 -->
      <path
        fill="#d4e8cc"
        opacity="0.9"
        d="M0,110 C200,60 400,130 650,75 C900,40 1150,100 1440,65 L1440,200 L0,200 Z"
      />
      <path
        fill="#c0ddb4"
        d="M0,140 C280,100 520,165 800,120 C1050,90 1280,130 1440,115 L1440,200 L0,200 Z"
      />
      <!-- 水田 -->
      <path fill="#b8d6a8" d="M0,155 L1440,155 L1440,200 L0,200 Z" />
      <!-- 稻穗轮廓（连续曲线，非一排图标） -->
      <path
        fill="#94c484"
        d="M0,155
           C40,135 80,150 120,132 C160,118 200,145 240,128
           C280,112 320,142 360,125 C400,108 440,138 480,122
           C520,106 560,136 600,120 C640,105 680,134 720,118
           C760,102 800,132 840,116 C880,100 920,130 960,114
           C1000,98 1040,128 1080,112 C1120,96 1160,126 1200,110
           C1240,94 1280,124 1320,108 C1360,92 1400,122 1440,115
           L1440,155 L0,155 Z"
      />
      <!-- 近处田埂高光 -->
      <path
        fill="#a8cf98"
        opacity="0.6"
        d="M0,168 C360,158 720,172 1080,162 C1260,157 1380,165 1440,160 L1440,200 L0,200 Z"
      />
    </svg>

    <!-- 水面微光 -->
    <div class="layer-shimmer"></div>

    <!-- 角落点缀 -->
    <Leaf class="accent accent-leaf" :size="accentSize" :stroke-width="1.5" />
    <Wheat class="accent accent-wheat" :size="accentSize" :stroke-width="1.5" />
    <Flower2 class="accent accent-flower" :size="accentSm" :stroke-width="1.5" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Leaf, Wheat, Flower2 } from 'lucide-vue-next'

const props = defineProps({
  variant: {
    type: String,
    default: 'chat',
    validator: (v) => ['home', 'chat', 'sidebar'].includes(v)
  }
})

const accentSize = computed(() => (props.variant === 'home' ? 22 : 18))
const accentSm = computed(() => (props.variant === 'home' ? 18 : 15))
</script>

<style lang="less" scoped>
.agri-scene {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.layer-sky {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    #e8f4fc 0%,
    #eef6f0 35%,
    #f2f7ee 70%,
    #edf3e9 100%
  );
}

.layer-sun {
  position: absolute;
  top: 5%;
  right: 10%;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: radial-gradient(
    circle at 35% 35%,
    #fff9e6 0%,
    #ffedb8 35%,
    rgba(255, 220, 150, 0.35) 65%,
    transparent 100%
  );
  opacity: 0.9;
}

.layer-clouds {
  position: absolute;
  inset: 0;
}

.cloud {
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  filter: blur(1px);
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.5);
}

.cloud::before,
.cloud::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: inherit;
}

.cloud-1 {
  top: 7%;
  left: 8%;
  width: 110px;
  height: 32px;
  opacity: 0.7;
  animation: cloud-drift 48s ease-in-out infinite;

  &::before {
    width: 44px;
    height: 44px;
    top: -16px;
    left: 16px;
  }

  &::after {
    width: 56px;
    height: 56px;
    top: -20px;
    right: 12px;
  }
}

.cloud-2 {
  top: 12%;
  right: 12%;
  width: 80px;
  height: 26px;
  opacity: 0.55;
  animation: cloud-drift 55s ease-in-out infinite reverse;
  animation-delay: -15s;

  &::before {
    width: 32px;
    height: 32px;
    top: -12px;
    left: 12px;
  }

  &::after {
    width: 40px;
    height: 40px;
    top: -14px;
    right: 10px;
  }
}

.cloud-3 {
  top: 4%;
  left: 42%;
  width: 64px;
  height: 20px;
  opacity: 0.45;
  animation: cloud-drift 42s ease-in-out infinite;
  animation-delay: -8s;

  &::before {
    width: 26px;
    height: 26px;
    top: -9px;
    left: 10px;
  }

  &::after {
    width: 32px;
    height: 32px;
    top: -11px;
    right: 8px;
  }
}

.cloud-4 {
  top: 18%;
  left: 22%;
  width: 48px;
  height: 16px;
  opacity: 0.38;
  animation: cloud-drift 38s ease-in-out infinite;
  animation-delay: -20s;

  &::before {
    width: 20px;
    height: 20px;
    top: -7px;
    left: 6px;
  }

  &::after {
    width: 24px;
    height: 24px;
    top: -9px;
    right: 5px;
  }
}

.cloud-5 {
  top: 16%;
  right: 32%;
  width: 56px;
  height: 18px;
  opacity: 0.35;
  animation: cloud-drift 50s ease-in-out infinite reverse;
  animation-delay: -25s;

  &::before {
    width: 22px;
    height: 22px;
    top: -8px;
    left: 8px;
  }

  &::after {
    width: 28px;
    height: 28px;
    top: -10px;
    right: 6px;
  }
}

@keyframes cloud-drift {
  0%,
  100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(20px);
  }
}

.bird {
  position: absolute;
  flex-shrink: 0;
  opacity: 0.45;
  animation: bird-glide 22s ease-in-out infinite;
}

.bird-1 {
  top: 11%;
  left: 28%;
}

.bird-2 {
  top: 16%;
  right: 24%;
  animation-delay: -7s;
  animation-direction: reverse;
}

.bird-3 {
  top: 8%;
  left: 58%;
  opacity: 0.3;
  animation-delay: -12s;
}

@keyframes bird-glide {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(12px, -3px);
  }
}

.layer-landscape {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 32%;
  min-height: 100px;
  max-height: 200px;
  display: block;
}

.layer-shimmer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 14%;
  min-height: 48px;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.08) 100%
  );
  mask-image: linear-gradient(180deg, transparent, black 80%);
}

.accent {
  position: absolute;
  color: #6b9478;
  opacity: 0.2;
}

.accent-leaf {
  top: 22%;
  left: 4%;
  transform: rotate(-20deg);
}

.accent-wheat {
  bottom: 32%;
  right: 5%;
  transform: rotate(10deg);
  opacity: 0.22;
}

.accent-flower {
  bottom: 38%;
  left: 7%;
  color: #b5a050;
  opacity: 0.18;
}

/* 对话页 */
.agri-scene--chat {
  .layer-landscape {
    height: 26%;
    max-height: 160px;
  }

  .layer-sun {
    width: 52px;
    height: 52px;
  }

  .cloud-4,
  .cloud-5,
  .bird-3 {
    display: none;
  }

  .accent-flower {
    display: none;
  }
}

/* 侧栏 */
.agri-scene--sidebar {
  .layer-sun,
  .layer-clouds,
  .bird,
  .accent {
    display: none;
  }

  .layer-sky {
    background: linear-gradient(180deg, #f0f5ec 0%, #e8efe4 100%);
  }

  .layer-landscape {
    height: 40%;
    max-height: 120px;
    opacity: 0.85;
  }

  .layer-shimmer {
    height: 20%;
  }
}

/* 首页 */
.agri-scene--home {
  .layer-landscape {
    height: 38%;
    max-height: 240px;
  }

  .layer-sun {
    width: 80px;
    height: 80px;
    top: 6%;
    right: 14%;
  }

  .cloud-1 {
    width: 140px;
  }

  .cloud-2 {
    width: 100px;
  }
}
</style>
