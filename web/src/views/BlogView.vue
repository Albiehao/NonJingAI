<template>
  <div class="blog-page">
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

    <main>
      <!-- Hero -->
      <section class="blog-hero">
        <div class="blog-hero-bg">
          <div class="blog-hero-image"></div>
          <div class="blog-hero-overlay"></div>
        </div>
        <div class="section-inner">
          <p class="section-label">Blog</p>
          <h1 class="page-title">技术博客</h1>
          <p class="page-desc">产品更新、使用指南与农业 AI 实践，帮助你更好地使用 {{ brandName }}。</p>
        </div>
      </section>

      <!-- Carousel -->
      <section class="carousel-section" v-if="featuredPosts.length">
        <div class="section-inner">
          <div class="carousel" ref="carouselRef">
            <div
              class="carousel-track"
              :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
            >
              <router-link
                v-for="post in featuredPosts"
                :key="post.slug"
                :to="`/blog/${post.slug}`"
                class="carousel-slide"
              >
                <div class="carousel-image">
                  <img :src="post.image" :alt="post.title" />
                </div>
                <div class="carousel-body">
                  <span class="carousel-cat">{{ post.category }}</span>
                  <h2 class="carousel-title">{{ post.title }}</h2>
                  <p class="carousel-summary">{{ post.summary }}</p>
                  <span class="carousel-more">阅读全文 <ArrowRight :size="15" /></span>
                </div>
              </router-link>
            </div>
          </div>
          <div class="carousel-dots">
            <button
              v-for="(post, i) in featuredPosts"
              :key="i"
              class="carousel-dot"
              :class="{ active: i === currentSlide }"
              @click="currentSlide = i"
            ></button>
          </div>
        </div>
      </section>

      <!-- Blog Grid -->
      <section class="blog-list-section">
        <div class="section-inner">
          <h2 class="list-title">全部文章</h2>
          <div class="blog-grid">
            <router-link
              v-for="post in blogPosts"
              :key="post.slug"
              :to="`/blog/${post.slug}`"
              class="blog-card"
            >
              <div class="blog-card-image">
                <img :src="post.image" :alt="post.title" />
                <span class="blog-card-cat">{{ post.category }}</span>
              </div>
              <div class="blog-card-body">
                <div class="blog-card-meta">
                  <time :datetime="post.date">{{ formatBlogDate(post.date) }}</time>
                  <span class="blog-card-dot">·</span>
                  <span>约 {{ post.readMinutes }} 分钟</span>
                </div>
                <h3 class="blog-card-title">{{ post.title }}</h3>
                <p class="blog-card-summary">{{ post.summary }}</p>
                <span class="blog-card-more">
                  阅读全文 <ArrowRight :size="15" />
                </span>
              </div>
            </router-link>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>&copy; {{ new Date().getFullYear() }} {{ brandName }}. All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from 'lucide-vue-next'
import UserInfoComponent from '@/components/UserInfoComponent.vue'
import { useInfoStore } from '@/stores/info'
import { useUserStore } from '@/stores/user'
import { blogPosts, getFeaturedPosts, formatBlogDate } from '@/data/blogPosts'

const router = useRouter()
const infoStore = useInfoStore()
const userStore = useUserStore()

const brandName = computed(
  () => infoStore.organization?.name || infoStore.branding?.name || '禾影千寻'
)

const featuredPosts = getFeaturedPosts()
const currentSlide = ref(0)

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
.blog-page {
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

/* ===== Hero ===== */
.blog-hero {
  position: relative;
  padding: 120px 0 0;
  overflow: hidden;
}

.blog-hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.blog-hero-image {
  position: absolute;
  inset: 0;
  background: url('/blog-bg.png') center / cover no-repeat;
}

.blog-hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.88);
}

.blog-hero .section-inner { position: relative; z-index: 1; }

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

.page-title {
  margin: 0 0 0.75rem;
  font-size: clamp(1.75rem, 3vw, 2.25rem);
  font-weight: 800;
  color: var(--gray-1000);
}

.page-desc {
  margin: 0 0 2.5rem;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--gray-600);
  max-width: 600px;
}

/* ===== Carousel ===== */
.carousel-section {
  padding: 2rem 0 1rem;
}

.carousel {
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid var(--gray-100);
  background: var(--gray-0);
}

.carousel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-slide {
  min-width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  text-decoration: none;
  color: inherit;
  min-height: 300px;
  max-height: 380px;
}

.carousel-image {
  overflow: hidden;
  background: var(--gray-50);
}

.carousel-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-body {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.carousel-cat {
  display: inline-block;
  padding: 3px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  background: var(--main-700);
  border-radius: 4px;
  margin-bottom: 1rem;
  align-self: flex-start;
}

.carousel-title {
  margin: 0 0 0.75rem;
  font-size: 1.4rem;
  font-weight: 700;
  line-height: 1.35;
  color: var(--gray-1000);
}

.carousel-summary {
  margin: 0 0 1rem;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--gray-600);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.carousel-more {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--main-700);
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 1rem;
}

.carousel-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  border: none;
  background: var(--gray-300);
  cursor: pointer;
  padding: 0;
  transition: background 0.2s;

  &.active {
    background: var(--main-600);
    width: 24px;
    border-radius: 4px;
  }
}

/* ===== Blog Grid ===== */
.blog-list-section {
  padding: 3rem 0 80px;
}

.list-title {
  margin: 0 0 1.5rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--gray-800);
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.blog-card {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--gray-100);
  border-radius: 8px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  background: var(--gray-0);
  transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 8px 24px var(--shadow-2); }
}

.blog-card-image {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: var(--gray-50);
}

.blog-card-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.blog-card-cat {
  position: absolute;
  top: 12px; left: 12px;
  padding: 3px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  border-radius: 4px;
}

.blog-card-body {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.blog-card-meta {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  color: var(--gray-500);
  margin-bottom: 0.5rem;
}

.blog-card-dot { opacity: 0.5; }

.blog-card-title {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--gray-1000);
  line-height: 1.4;
}

.blog-card-summary {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--gray-600);
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-card-more {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--main-700);
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

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .carousel-slide {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .carousel-image {
    aspect-ratio: 16 / 9;
  }

  .carousel-body {
    padding: 1.5rem;
  }
}

/* ========== Dark Mode ========== */
:root.dark .blog-page {
  background: #0a0a0a;
}

:root.dark .navbar {
  background: rgba(10, 10, 10, 0.88);
  border-bottom-color: var(--gray-150);
}

:root.dark .blog-hero-overlay {
  background: rgba(0, 0, 0, 0.65);
}

:root.dark .blog-hero .page-title {
  color: var(--gray-2000);
}

:root.dark .carousel {
  background: #0d0d0d;
  border-color: var(--gray-150);
}

:root.dark .carousel-body {
  background: #0d0d0d;
}

:root.dark .carousel-title {
  color: var(--gray-2000);
}

:root.dark .blog-card {
  background: #0d0d0d;
  border-color: var(--gray-150);
}

:root.dark .blog-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

:root.dark .blog-card-title {
  color: var(--gray-2000);
}

:root.dark .list-title {
  color: var(--gray-800);
}

:root.dark .footer {
  background: #0d0d0d;
  border-top-color: var(--gray-150);
}

@media (max-width: 768px) {
  .navbar-inner { padding: 0 1.25rem; }
  .navbar-links { display: none; }
  .section-inner { padding: 0 1.25rem; }

  .blog-hero { padding: 100px 0 0; }

  .blog-grid {
    grid-template-columns: 1fr;
  }

  .blog-list-section { padding: 2rem 0 60px; }
}
</style>
