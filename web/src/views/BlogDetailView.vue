<template>
  <div class="blog-detail-page">
    <header class="navbar">
      <div class="navbar-inner">
        <router-link to="/" class="navbar-brand">
          <img src="/logo.png" alt="logo" class="brand-icon" />
          <span class="brand-name">{{ brandName }}</span>
        </router-link>
        <nav class="navbar-links">
          <router-link to="/" class="nav-link">主页</router-link>
          <a href="/agent" class="nav-link" @click.prevent="requireAuth('/agent')">Agent</a>
          <a href="/graph" class="nav-link" @click.prevent="requireAuth('/graph')">图谱</a>
          <router-link to="/blog" class="nav-link active">博客</router-link>
        </nav>
        <div class="navbar-actions">
          <UserInfoComponent :show-button="true" />
        </div>
      </div>
    </header>

    <main v-if="post" class="article-main">
      <div class="article-bg">
        <div class="article-bg-image"></div>
        <div class="article-bg-overlay"></div>
      </div>

      <div class="article-back">
        <div class="section-inner">
          <router-link to="/blog" class="back-link">
            <ArrowLeft :size="16" />
            返回博客列表
          </router-link>
        </div>
      </div>

      <article class="article-content">
        <div class="section-inner">
          <header class="article-head">
            <div class="article-image">
              <img :src="post.image" :alt="post.title" />
              <span class="article-cat">{{ post.category }}</span>
            </div>
            <div class="article-head-body">
              <div class="article-meta">
                <time :datetime="post.date">{{ formatBlogDate(post.date) }}</time>
                <span class="meta-dot">·</span>
                <span>约 {{ post.readMinutes }} 分钟</span>
              </div>
              <h1 class="article-title">{{ post.title }}</h1>
              <p class="article-lead">{{ post.summary }}</p>
            </div>
          </header>

          <div class="article-body">
            <MdPreview :modelValue="post.content" previewTheme="github" class="article-md" />
          </div>
        </div>
      </article>
    </main>

    <main v-else class="article-main not-found">
      <div class="section-inner">
        <h1>文章不存在</h1>
        <router-link to="/blog" class="back-btn">返回博客列表</router-link>
      </div>
    </main>

    <footer class="footer">
      <p>&copy; {{ new Date().getFullYear() }} {{ brandName }}. All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import UserInfoComponent from '@/components/UserInfoComponent.vue'
import { useInfoStore } from '@/stores/info'
import { useUserStore } from '@/stores/user'
import { getBlogPost, formatBlogDate } from '@/data/blogPosts'

const route = useRoute()
const router = useRouter()
const infoStore = useInfoStore()
const userStore = useUserStore()

const brandName = computed(
  () => infoStore.organization?.name || infoStore.branding?.name || '禾影千寻'
)

const post = computed(() => getBlogPost(route.params.slug))

const requireAuth = (path) => {
  if (userStore.isLoggedIn) {
    router.push(path)
  } else {
    sessionStorage.setItem('redirect', path)
    router.push('/login')
  }
}
</script>

<style lang="less" scoped>
.blog-detail-page {
  min-height: 100vh;
  background: var(--gray-10);
  color: var(--gray-1000);
  overflow-x: hidden;
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
  text-decoration: none;
  color: inherit;
}

.brand-icon { width: 32px; height: 32px; }
.brand-name { font-size: 1.1rem; font-weight: 700; }

.navbar-links { display: flex; gap: 2rem; }

.nav-link {
  font-size: 0.9rem;
  color: var(--gray-600);
  text-decoration: none;
  &:hover { color: var(--main-color); }
  &.active { color: var(--main-700); font-weight: 600; }
}

.navbar-actions :deep(.ant-btn-primary) {
  background: var(--main-700);
  border-color: var(--main-700);
  border-radius: 999px;
  padding-inline: 1.25rem;
  height: 34px;
}

/* ===== Background ===== */
.article-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.article-bg-image {
  position: absolute;
  inset: 0;
  background: url('/blog-bg.png') center / cover no-repeat;
}

.article-bg-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.88);
}

/* ===== Back ===== */
.article-back {
  position: relative;
  z-index: 1;
  padding-top: 80px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  color: var(--gray-500);
  text-decoration: none;
  padding: 6px 0;
  &:hover { color: var(--main-700); }
}

/* ===== Article ===== */
.article-main {
  position: relative;
  z-index: 1;
  flex: 1;
  padding-bottom: 3rem;

  &.not-found {
    text-align: center;
    padding-top: 120px;
    h1 { margin-bottom: 1rem; }
  }
}

.section-inner {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.article-content {
  padding-top: 2rem;
}

.article-head {
  background: var(--gray-0);
  border: 1px solid var(--gray-100);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.article-image {
  position: relative;
  width: 100%;
  aspect-ratio: 21 / 9;
  overflow: hidden;
  background: var(--gray-50);
}

.article-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-cat {
  position: absolute;
  top: 16px; left: 16px;
  padding: 4px 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #fff;
  background: var(--main-700);
  border-radius: 4px;
}

.article-head-body {
  padding: 1.5rem 2rem 2rem;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  color: var(--gray-500);
}

.meta-dot { opacity: 0.5; }

.article-title {
  margin: 0 0 1rem;
  font-size: 1.85rem;
  font-weight: 800;
  line-height: 1.3;
  letter-spacing: -0.02em;
  color: var(--gray-1000);
}

.article-lead {
  margin: 0;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--gray-600);
}

/* ===== Body MD ===== */
.article-body {
  background: var(--gray-0);
  border: 1px solid var(--gray-100);
  border-radius: 8px;
  padding: 2rem;

  :deep(.article-md) {
    background: transparent;
  }

  :deep(.md-editor-preview-wrapper) {
    padding: 0;
  }

  :deep(.md-editor-preview) {
    font-size: 1rem;
    line-height: 1.8;
    color: var(--gray-800);
  }

  :deep(h2) {
    margin: 2rem 0 0.75rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--gray-1000);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--gray-100);
  }

  :deep(h3) {
    margin: 1.5rem 0 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--gray-900);
  }

  :deep(p) {
    margin: 0 0 1rem;
  }

  :deep(ul),
  :deep(ol) {
    padding-left: 1.5rem;
    margin: 0 0 1rem;
  }

  :deep(li) {
    margin-bottom: 0.35rem;
    line-height: 1.7;
  }

  :deep(strong) {
    color: var(--gray-1000);
    font-weight: 600;
  }

  :deep(code) {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.9em;
    background: var(--gray-50);
    padding: 2px 6px;
    border-radius: 3px;
    color: var(--gray-900);
  }

  :deep(pre code) {
    background: none;
    padding: 0;
  }
}

.back-btn {
  display: inline-block;
  color: var(--main-700);
  font-weight: 600;
  text-decoration: none;
  &:hover { text-decoration: underline; }
}

/* ===== Footer ===== */
.footer {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  font-size: 0.85rem;
  color: var(--gray-500);
  background: var(--gray-0);
  border-top: 1px solid var(--gray-100);
}

/* ===== Responsive ===== */
/* ========== Dark Mode ========== */
:root.dark .blog-detail-page {
  background: #0a0a0a;
}

:root.dark .navbar {
  background: rgba(10, 10, 10, 0.88);
  border-bottom-color: var(--gray-150);
}

:root.dark .article-bg-overlay {
  background: rgba(0, 0, 0, 0.65);
}

:root.dark .article-title {
  color: var(--gray-2000);
}

:root.dark .article-head {
  background: #0d0d0d;
  border-color: var(--gray-150);
}

:root.dark .article-body {
  background: #0d0d0d;
  border-color: var(--gray-150);
}

:root.dark .footer {
  background: #0d0d0d;
  border-top-color: var(--gray-150);
}

@media (max-width: 768px) {
  .navbar-inner { padding: 0 1.25rem; }
  .navbar-links { display: none; }
  .section-inner { padding: 0 1.25rem; }

  .article-head-body { padding: 1.25rem; }
  .article-title { font-size: 1.4rem; }
  .article-body { padding: 1.25rem; }
}
</style>
