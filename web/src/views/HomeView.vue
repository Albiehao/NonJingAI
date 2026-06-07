<template>
  <div class="home">
    <div v-if="isLoading" class="loading-state">
      <a-spin size="large" />
      <p>正在连接服务...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <a-result status="error" :title="error.title" :sub-title="error.message">
        <template #extra>
          <a-button type="primary" @click="retryLoad">重试</a-button>
        </template>
      </a-result>
    </div>

    <template v-else>
      <header class="navbar">
        <div class="navbar-inner">
          <div class="navbar-brand">
            <img src="/logo.png" alt="logo" class="brand-icon" />
            <span class="brand-name">{{ brandName }}</span>
          </div>
          <nav class="navbar-links">
            <router-link to="/" class="nav-link">主页</router-link>
            <a href="/agent" class="nav-link" @click.prevent="requireAuth('/agent')">Agent</a>
            <a href="/graph" class="nav-link" @click.prevent="requireAuth('/graph')">图谱</a>
            <router-link to="/blog" class="nav-link">博客</router-link>
          </nav>
          <div class="navbar-actions">
            <UserInfoComponent :show-button="true" />
          </div>
        </div>
      </header>

      <main>
        <!-- ===== Hero ===== -->
        <section class="hero">
          <div class="hero-bg">
            <div class="hero-bg-image"></div>
            <div class="hero-bg-overlay"></div>
            <div class="hero-glow glow-1"></div>
            <div class="hero-glow glow-2"></div>
          </div>
          <div class="hero-inner">
            <div class="hero-left">
<h1 class="hero-title">{{ brandName }}</h1>
              <p class="hero-subtitle">基于大模型、知识图谱与视觉识别的智能分析平台</p>
              <p class="hero-desc">
                融合 RAG、知识图谱、YOLO 图像识别与 Agent 推理，通过多步骤工作流连接工具，实现从文档到决策的一体化分析。
              </p>
              <div class="hero-actions">
                <button class="btn btn-primary" @click="goToChat">
                  <MessageCircle :size="18" />
                  开始对话
                </button>
                <button class="btn btn-ghost" @click="scrollTo('agent')">
                  <Braces :size="18" />
                  了解能力
                </button>
              </div>
            </div>
            <div class="hero-right">
              <video
                ref="heroVideo"
                src="/video.mp4"
                muted
                loop
                autoplay
                playsinline
                class="hero-video"
              ></video>
            </div>
          </div>
        </section>

        <!-- ===== Agent ===== -->
        <section id="agent" class="agent-section">
          <div class="section-inner">
            <div class="section-header">
              <p class="section-label">Agent 引擎</p>
              <h2 class="section-title">智能体编排</h2>
              <p class="section-desc">
                基于 LangGraph 构建多步骤 Agent 工作流，支持工具调用、附件处理、上下文持久化与思考模式。
              </p>
            </div>
            <div class="agent-grid">
              <div v-for="card in agentFeatures" :key="card.title" class="agent-card">
                <div class="agent-card-icon">
                  <component :is="card.icon" :size="24" />
                </div>
                <h3 class="agent-card-title">{{ card.title }}</h3>
                <p class="agent-card-desc">{{ card.desc }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- ===== Knowledge Graph ===== -->
        <section id="kg" class="kg-section">
          <div class="section-inner">
            <div class="kg-layout">
              <div class="kg-image">
                <img src="/tupu.png" alt="知识图谱" />
              </div>
              <div class="kg-content">
                <p class="section-label">知识图谱</p>
                <h2 class="section-title">结构化知识关联</h2>
                <p class="section-desc">
                  基于知识图谱技术，自动提取实体与关系，构建结构化知识网络。支持图谱查询、路径分析与智能推理，让 AI 的回答更具可解释性。
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- ===== YOLO / 视觉识别 ===== -->
        <section class="yolo-section">
          <div class="section-inner">
            <div class="yolo-layout">
              <div class="yolo-content">
                <p class="section-label">视觉识别</p>
                <h2 class="section-title">YOLO 目标检测</h2>
                <p class="section-desc">
                  集成 YOLO 视觉识别模型，支持图像中的目标检测、定位与分类。可智能识别农田作物、病虫害、设备仪表等对象，为农业分析提供视觉数据支撑。
                </p>
              </div>
              <div class="yolo-image">
                <img src="/yolo.png" alt="YOLO视觉识别" />
              </div>
            </div>
          </div>
        </section>

        <!-- ===== 报告生成 ===== -->
        <section class="report-section">
          <div class="section-inner">
            <div class="report-layout">
              <div class="report-image">
                <img src="/bao.png" alt="报告生成" />
              </div>
              <div class="report-content">
                <p class="section-label">报告生成</p>
                <h2 class="section-title">智能分析报告</h2>
                <p class="section-desc">
                  基于多源数据融合与 Agent 推理，自动生成结构化的农田分析报告。涵盖作物状态评估、病虫害诊断、防治建议与产量预测，辅助农业决策。
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- ===== AI 对话 ===== -->
        <section class="chat-section">
          <div class="section-inner">
            <div class="chat-layout">
              <div class="chat-content">
                <p class="section-label">AI 对话</p>
                <h2 class="section-title">智能问诊</h2>
                <p class="section-desc">
                  基于大语言模型与农业知识库，支持自然语言交互的智能问诊。上传作物图片、描述症状，AI 自动识别病虫害并提供防治建议与处方方案。
                </p>
              </div>
              <div class="chat-image">
                <img src="/chat.png" alt="AI智能问诊" />
              </div>
            </div>
          </div>
        </section>

        <!-- ===== 灾害预警 ===== -->
        <section class="alert-section">
          <div class="section-inner">
            <div class="section-header">
              <p class="section-label">灾害预警</p>
              <h2 class="section-title">农业生产灾害预警推送</h2>
              <p class="section-desc">
                基于气象数据与农田信息，提供个性化的灾害预警推送服务。更懂你的农田，更精准的预警 — 支持邮箱自动推送，第一时间获取低温冻害、暴雨渍涝、大风倒伏等灾害通知，防患于未然。
              </p>
            </div>
            <div class="alert-grid">
              <div class="alert-card">
                <div class="alert-card-icon"><Bell :size="24" /></div>
                <h3 class="alert-card-title">个性化推送</h3>
                <p class="alert-card-desc">针对你的作物类型与种植区域，推送最相关的灾害预警，不打扰、不遗漏。</p>
              </div>
              <div class="alert-card">
                <div class="alert-card-icon"><Mail :size="24" /></div>
                <h3 class="alert-card-title">邮箱自动推送</h3>
                <p class="alert-card-desc">绑定邮箱即可自动接收预警通知，重要灾害信息直达 inbox。</p>
              </div>
              <div class="alert-card">
                <div class="alert-card-icon"><Shield :size="24" /></div>
                <h3 class="alert-card-title">多灾种覆盖</h3>
                <p class="alert-card-desc">支持低温冻害、暴雨渍涝、大风倒伏、干旱等多种农业生产灾害预警。</p>
              </div>
            </div>
          </div>
        </section>

        <!-- ===== CTA ===== -->
        <section class="cta-section">
          <div class="section-inner">
            <div class="cta-banner">
              <div class="cta-text">
                <h2 class="cta-title">准备好开始了吗？</h2>
                <p class="cta-desc">进入 {{ brandName }}，体验智能体驱动的一体化分析能力。</p>
              </div>
              <button class="btn btn-primary btn-lg" @click="goToChat">
                <MessageCircle :size="20" />
                开始对话
              </button>
            </div>
          </div>
        </section>

        <!-- ===== Blog ===== -->
        <section class="blog-section">
          <div class="section-inner">
            <div class="blog-head">
              <div class="blog-head-left">
                <p class="section-label">技术博客</p>
                <h2 class="section-title">最新文章</h2>
              </div>
              <router-link to="/blog" class="blog-link">
                查看全部 <ArrowRight :size="16" />
              </router-link>
            </div>
            <div class="blog-grid">
              <router-link
                v-for="post in previewPosts"
                :key="post.slug"
                :to="`/blog/${post.slug}`"
                class="blog-card"
              >
                <span class="blog-card-cat">{{ post.category }}</span>
                <h3 class="blog-card-title">{{ post.title }}</h3>
                <p class="blog-card-summary">{{ post.summary }}</p>
              </router-link>
            </div>
          </div>
        </section>
      </main>

      <footer class="footer">
        <div class="footer-qr">
          <img src="/gzh.jpg" alt="微信公众号" class="qr-img" />
          <span class="qr-label">扫码关注微信公众号</span>
        </div>
        <p>&copy; {{ new Date().getFullYear() }} {{ brandName }}. All Rights Reserved.</p>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useInfoStore } from '@/stores/info'
import { useAgentStore } from '@/stores/agent'
import { healthApi } from '@/apis/system_api'
import { blogPosts } from '@/data/blogPosts'
import { Result, Button, Spin } from 'ant-design-vue'
import UserInfoComponent from '@/components/UserInfoComponent.vue'
import {
  MessageCircle,
  Braces,
  Workflow,
  Brain,
  Wrench,
  ArrowRight,
  Bell,
  Mail,
  Shield
} from 'lucide-vue-next'

const AResult = Result
const AButton = Button
const ASpin = Spin

const router = useRouter()
const userStore = useUserStore()
const infoStore = useInfoStore()
const agentStore = useAgentStore()

const isLoading = ref(true)
const error = ref(null)
const heroVideo = ref(null)

const brandName = computed(
  () => infoStore.organization?.name || infoStore.branding?.name || '禾影千寻'
)

const agentFeatures = [
  {
    icon: Workflow,
    title: '多步骤推理',
    desc: '基于 LangGraph 构建多步骤 Agent 工作流，智能体自主规划执行路径，逐步推理得出结论。'
  },
  {
    icon: Wrench,
    title: '工具调用',
    desc: '支持动态调用知识库检索、图谱查询、联网搜索、YOLO 识别、计算器、天气等多种工具协同工作。'
  },
  {
    icon: Brain,
    title: '深度思考',
    desc: '通过 Agent 编排大模型，调查农田问题并生成报告'
  }
]

const previewPosts = computed(() => blogPosts.slice(0, 3))

const checkHealth = async () => {
  try {
    const res = await healthApi.checkHealth()
    if (res.status !== 'ok') throw new Error('服务不可用')
  } catch (e) {
    error.value = { title: '服务连接失败', message: '后端服务无法响应，请检查服务是否正常运行' }
    throw e
  }
}

const loadData = async () => {
  isLoading.value = true
  error.value = null
  try {
    await checkHealth()
    await infoStore.loadInfoConfig()
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    isLoading.value = false
  }
}

const retryLoad = () => loadData()
const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })

const requireAuth = (path) => {
  if (userStore.isLoggedIn) {
    router.push(path)
  } else {
    sessionStorage.setItem('redirect', path)
    router.push('/login')
  }
}

const goToChat = async () => {
  if (!userStore.isLoggedIn) {
    sessionStorage.setItem('redirect', '/')
    router.push('/login')
    return
  }
  if (userStore.isAdmin) {
    router.push('/agent')
    return
  }
  try {
    const defaultAgent = agentStore.defaultAgent
    if (defaultAgent?.id) {
      router.push(`/agent/${defaultAgent.id}`)
    } else {
      router.push('/agent')
    }
  } catch {
    router.push('/')
  }
}

onMounted(() => { loadData() })
</script>

<style lang="less" scoped>
.home {
  min-height: 100vh;
  background: var(--gray-10);
  color: var(--gray-1000);
  overflow-x: hidden;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 1rem;
}

/* ===== Navbar ===== */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--gray-100);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.brand-icon {
  width: 32px; height: 32px;
}

.brand-name {
  font-size: 1.1rem;
  font-weight: 700;
}

.navbar-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  font-size: 0.9rem;
  color: var(--gray-600);
  text-decoration: none;
  &:hover { color: var(--main-color); }
}

.navbar-actions :deep(.ant-btn-primary) {
  background: var(--main-700);
  border-color: var(--main-700);
  border-radius: 999px;
  padding-inline: 1.25rem;
  height: 34px;
}

/* ===== Hero ===== */
.hero {
  position: relative;
  padding: 140px 0 100px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.hero-bg-image {
  position: absolute;
  inset: 0;
  background: url('/home-bg.jpg') center / cover no-repeat;
}

.hero-bg-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.88);
}

.hero-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
}

.glow-1 {
  width: 700px; height: 700px;
  background: var(--main-300);
  top: -300px; right: -200px;
}

.glow-2 {
  width: 500px; height: 500px;
  background: var(--color-accent-500);
  bottom: -200px; left: -100px;
}

.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 4px 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--main-700);
  background: var(--main-10);
  border: 1px solid var(--main-100);
  border-radius: 999px;
  margin-bottom: 1rem;
}

.hero-title {
  margin: 0;
  font-size: clamp(2.6rem, 4.5vw, 3.6rem);
  font-weight: 800;
  line-height: 1.1;
  color: var(--gray-1000);
}

.hero-subtitle {
  margin: 0.75rem 0 0.5rem;
  font-size: clamp(1.05rem, 2vw, 1.3rem);
  font-weight: 600;
  color: var(--main-700);
}

.hero-desc {
  margin: 0 0 1.5rem;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--gray-600);
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* Hero Right Video */
.hero-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-video {
  display: block;
  width: 100%;
  max-width: 520px;
  border-radius: 12px;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  background: #000;
}

/* ===== Buttons ===== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.65rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background 0.2s, border-color 0.2s;
}

.btn-primary {
  background: var(--main-700);
  color: #fff;
  border-color: var(--main-700);
  &:hover { background: var(--main-800); }
}

.btn-ghost {
  background: var(--gray-0);
  color: var(--gray-800);
  border-color: var(--gray-200);
  &:hover { border-color: var(--main-300); color: var(--main-700); }
}

.btn-lg {
  padding: 0.85rem 2rem;
  font-size: 1.05rem;
}

/* ===== Section ===== */
.section-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-label {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--main-600);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin: 0 0 0.5rem;
}

.section-title {
  margin: 0 0 0.75rem;
  font-size: clamp(1.75rem, 3vw, 2.25rem);
  font-weight: 800;
  line-height: 1.25;
  color: var(--gray-1000);
}

.section-desc {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--gray-600);
}

.section-header {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 48px;
}

/* ===== Agent ===== */
.agent-section {
  padding: 80px 0;
  background: var(--gray-0);
}

.agent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.agent-card {
  padding: 2rem;
  border: 1px solid var(--gray-100);
  border-radius: 8px;
  transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 8px 24px var(--shadow-2); }
}

.agent-card-icon {
  width: 48px; height: 48px;
  border-radius: 8px;
  background: var(--main-10);
  color: var(--main-700);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.agent-card-title {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--gray-900);
}

.agent-card-desc {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--gray-600);
}

/* ===== Knowledge Graph ===== */
.kg-section {
  padding: 80px 0;
  background: var(--gray-0);
}

.kg-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.kg-image {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-100);
}

.kg-image img {
  display: block;
  width: 100%;
  height: auto;
}

.kg-content .section-title {
  margin: 0 0 1rem;
}

/* ===== YOLO ===== */
.yolo-section {
  padding: 80px 0;
  background: var(--gray-10);
}

.yolo-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.yolo-image {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-100);
}

.yolo-image img {
  display: block;
  width: 100%;
  height: auto;
}

.yolo-content .section-title {
  margin: 0 0 1rem;
}

/* ===== Report ===== */
.report-section {
  padding: 80px 0;
  background: var(--gray-0);
}

.report-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.report-image {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-100);
}

.report-image img {
  display: block;
  width: 100%;
  height: auto;
}

.report-content .section-title {
  margin: 0 0 1rem;
}

/* ===== AI Chat ===== */
.chat-section {
  padding: 80px 0;
  background: var(--gray-10);
}

.chat-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.chat-image {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-100);
}

.chat-image img {
  display: block;
  width: 100%;
  height: auto;
}

.chat-content .section-title {
  margin: 0 0 1rem;
}

/* ===== 灾害预警 ===== */
.alert-section {
  padding: 80px 0;
  background: var(--gray-10);
}

.alert-section .section-header {
  margin-bottom: 3rem;
}

.alert-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.alert-card {
  padding: 1.5rem;
  border-radius: 8px;
  background: var(--gray-0);
  border: 1px solid var(--gray-100);
}

.alert-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: var(--main-50);
  color: var(--main-600);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.alert-card-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--gray-1000);
  margin: 0 0 0.5rem;
}

.alert-card-desc {
  font-size: 0.9rem;
  color: var(--gray-600);
  line-height: 1.6;
  margin: 0;
}

/* ===== CTA ===== */
.cta-section {
  padding: 60px 0;
  background: var(--gray-0);
}

.cta-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 2.5rem 3rem;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--main-700) 0%, var(--main-800) 100%);
  color: #fff;
}

.cta-title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.cta-desc {
  margin: 0;
  font-size: 0.95rem;
  opacity: 0.85;
  line-height: 1.5;
}

.cta-banner .btn-primary {
  background: #fff;
  color: var(--main-700);
  border-color: #fff;
  &:hover { background: var(--gray-50); }
}

/* ===== Blog ===== */
.blog-section {
  padding: 80px 0;
  background: var(--gray-0);
}

.blog-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.blog-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--main-700);
  text-decoration: none;
  flex-shrink: 0;
  &:hover { color: var(--main-800); }
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.blog-card {
  display: block;
  padding: 1.5rem;
  border: 1px solid var(--gray-100);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 8px 24px var(--shadow-2); }
}

.blog-card-cat {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--main-600);
  margin-bottom: 0.5rem;
}

.blog-card-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.4;
  color: var(--gray-1000);
}

.blog-card-summary {
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--gray-600);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ===== Footer ===== */
.footer {
  text-align: center;
  padding: 2rem;
  font-size: 0.85rem;
  color: var(--gray-500);
  background: var(--gray-0);
  border-top: 1px solid var(--gray-100);
}

.footer-qr {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.qr-img {
  width: 100px;
  height: 100px;
  border-radius: 8px;
}

.qr-label {
  font-size: 0.8rem;
  color: var(--gray-400);
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .hero-inner {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-right {
    order: -1;
  }

  .hero-video {
    max-width: 100%;
  }

  .agent-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .kg-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .kg-image {
    order: -1;
  }

  .yolo-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .yolo-image {
    order: -1;
  }

  .report-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .chat-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .chat-image {
    order: -1;
  }
}

/* ========== Dark Mode ========== */
:root.dark .home {
  background: #0a0a0a;
}

:root.dark .navbar {
  background: rgba(10, 10, 10, 0.88);
  border-bottom-color: var(--gray-150);
}

:root.dark .hero-bg-overlay {
  background: rgba(0, 0, 0, 0.65);
}

:root.dark .hero-title {
  color: var(--gray-2000);
}

:root.dark .agent-section,
:root.dark .kg-section,
:root.dark .report-section,
:root.dark .blog-section,
:root.dark .cta-section {
  background: #0d0d0d;
}

:root.dark .yolo-section,
:root.dark .chat-section {
  background: #0a0a0a;
}

:root.dark .agent-card {
  border-color: var(--gray-150);
}

:root.dark .agent-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

:root.dark .blog-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

:root.dark .btn-ghost {
  background: rgba(30, 30, 30, 0.6);
  border-color: var(--gray-150);
  color: var(--gray-800);
}

:root.dark .btn-ghost:hover {
  border-color: var(--main-400);
  color: var(--main-400);
}

:root.dark .cta-banner .btn-primary {
  background: var(--main-700);
  color: #fff;
}

:root.dark .cta-banner .btn-primary:hover {
  background: var(--main-600);
}

:root.dark .footer {
  background: #0d0d0d;
  border-top-color: var(--gray-150);
}

:root.dark .kg-image,
:root.dark .yolo-image,
:root.dark .report-image,
:root.dark .chat-image {
  border-color: var(--gray-150);
}

@media (max-width: 768px) {
  .navbar-inner { padding: 0 1.25rem; }
  .navbar-links { display: none; }

  .hero { padding: 100px 0 60px; }
  .agent-section { padding: 60px 0; }
  .kg-section { padding: 60px 0; }
  .yolo-section { padding: 60px 0; }
  .report-section { padding: 60px 0; }
  .chat-section { padding: 60px 0; }
  .blog-section { padding: 60px 0; }
  .section-inner { padding: 0 1.25rem; }

  .agent-grid,
  .blog-grid {
    grid-template-columns: 1fr;
  }

  .cta-banner {
    flex-direction: column;
    text-align: center;
    padding: 2rem 1.5rem;
  }
}
</style>
