<template>
  <div class="login-banner">
    <div class="banner-bg">
      <img :src="loginBgImage" alt="登录背景" />
    </div>
    <div class="banner-overlay">
      <div class="banner-content">
        <h1 class="banner-title">
          <span v-if="brandOrgName" class="banner-org">{{ brandOrgName }}</span>
          <span class="banner-brand">{{ brandName }}</span>
        </h1>
        <p class="banner-subtitle">{{ brandSubtitle }}</p>
        <p class="banner-desc">{{ brandDescription }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useInfoStore } from '@/stores/info'

const infoStore = useInfoStore()

const loginBgImage = computed(() => {
  return infoStore.organization?.login_bg || '/farm-bg.jpg'
})
const brandOrgName = computed(() => {
  return infoStore.organization?.name?.trim() || ''
})
const brandName = computed(() => {
  const orgName = brandOrgName.value
  const brandNameRaw = infoStore.branding?.name?.trim() || 'QianXun'
  if (orgName && brandNameRaw && orgName !== brandNameRaw) return brandNameRaw
  return orgName || brandNameRaw
})
const brandSubtitle = computed(() => {
  const raw = infoStore.branding?.subtitle ?? ''
  return raw.trim() || '大模型驱动的多模态智能 Agent 平台'
})
const brandDescription = computed(() => {
  const raw = infoStore.branding?.description ?? ''
  return raw.trim() || '融合 RAG 知识库、知识图谱与多模态识别，以 Agent 驱动智能分析与决策'
})
</script>

<style lang="less" scoped>
.login-banner {
  flex: 1;
  max-width: 50%;
  position: relative;
  overflow: hidden;
  display: none;

  @media (min-width: 1024px) {
    display: block;
  }
}

.banner-bg {
  position: absolute;
  inset: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(46, 125, 50, 0.85) 0%, rgba(46, 125, 50, 0.35) 100%);
  }
}

.banner-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  padding: 80px;
  z-index: 1;
}

.banner-content {
  max-width: 520px;
}

.banner-title {
  margin: 0 0 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;

  .banner-org {
    font-size: 16px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .banner-brand {
    font-size: 36px;
    font-weight: 700;
    color: #fff;
    line-height: 1.2;
  }
}

.banner-subtitle {
  font-size: 20px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 12px;
  line-height: 1.4;
}

.banner-desc {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  line-height: 1.6;
}
</style>
