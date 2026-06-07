<template>
  <div class="home-page" :class="{ 'light-mode': isLightMode }">
    <main class="home-main">
      <section class="hero">
        <div class="hero-carousel-full" aria-label="首页轮播图">
          <div class="hero-slide-stage" :style="{ '--slide-dir': slideDir }">
            <div class="hero-slide-media">
              <!-- 预留图片位：把 image 替换为你的图片路径即可 -->
              <transition name="hero-slide-media" mode="out-in">
                <img
                  v-if="heroSlides[currentSlide].image"
                  :key="`media-${currentSlide}`"
                  class="hero-slide-img"
                  :src="heroSlides[currentSlide].image"
                  :alt="heroSlides[currentSlide].title"
                />
                <div v-else :key="`placeholder-${currentSlide}`" class="hero-slide-placeholder">
                  <p class="placeholder-badge">待替换轮播图</p>
                  <p class="placeholder-title">{{ heroSlides[currentSlide].title }}</p>
                  <p class="placeholder-tip">在 `public/hero-slides.json` 里填写 image 路径即可替换</p>
                </div>
              </transition>
            </div>

            <transition name="hero-slide-text" mode="out-in">
              <div :key="`text-${currentSlide}`" class="hero-slide-info hero-slide-info--overlay">
                <p class="hero-tag"><span class="hero-tag-dot" aria-hidden="true"></span>{{ heroSlides[currentSlide].kicker }}</p>
                <h1 class="hero-title">{{ heroSlides[currentSlide].title }}</h1>
                <p class="hero-desc">{{ heroSlides[currentSlide].text }}</p>
              </div>
            </transition>
          </div>
          <div class="hero-slide-controls">
            <button class="carousel-nav prev" type="button" @click="prevSlide" aria-label="上一张">‹</button>
            <div class="carousel-dots">
              <button
                v-for="(slide, idx) in heroSlides"
                :key="slide.id"
                class="dot"
                :class="{ active: idx === currentSlide }"
                type="button"
                :aria-label="`切换到第 ${idx + 1} 张`"
                @click="goToSlide(idx)"
              ></button>
            </div>
            <button class="carousel-nav next" type="button" @click="nextSlide" aria-label="下一张">›</button>
          </div>
        </div>
      </section>

      <section class="gallery">
        <h2 class="section-title">数据与渠道展示</h2>
        <div class="gallery-grid">
          <article v-for="card in galleryCards" :key="card.id" class="showcase-card">
            <div class="showcase-top">
              <span class="showcase-dot"></span>
              <span class="showcase-dot"></span>
              <span class="showcase-dot"></span>
              <p class="showcase-status">{{ card.status }}</p>
            </div>
            <div class="showcase-screen">
              <img class="showcase-img" :src="card.image" :alt="card.title" />
            </div>
            <p class="showcase-title">{{ card.title }}</p>
            <p class="showcase-text">{{ card.text }}</p>
          </article>
        </div>
      </section>

      <section class="pesticide">
        <h2 class="section-title">农药介绍</h2>
        <div class="pesticide-grid">
          <article v-for="p in pesticides" :key="p.id" class="pesticide-card">
            <div class="pesticide-media">
              <img class="pesticide-img" :src="p.image" :alt="p.name" />
            </div>
            <div class="pesticide-head">
              <div>
                <p class="pesticide-name">
                  {{ p.name }}
                  <span v-if="p.enName" class="pesticide-en">（{{ p.enName }}）</span>
                </p>
              </div>
              <p class="pesticide-badge">{{ p.type }}</p>
            </div>
            <p class="pesticide-desc">{{ p.summary }}</p>
            <ul class="pesticide-meta">
              <li><span class="k">对象</span><span class="v">{{ p.targets }}</span></li>
              <li><span class="k">作物</span><span class="v">{{ p.crops }}</span></li>
              <li><span class="k">用法</span><span class="v">{{ p.usage }}</span></li>
              <li><span class="k">注意</span><span class="v">{{ p.notes }}</span></li>
            </ul>
          </article>
        </div>
        <div class="pesticide-more">
          <hm-button class="more-btn" label="访问更多" type="button" @click="handleMorePesticides" />
        </div>
      </section>

      <section class="testimonials">
        <div class="testimonials-head">
          <p class="testimonials-kicker">Loved by users</p>
          <h2 class="testimonials-title">用户评价展示</h2>
          <p class="testimonials-subtitle">滚动浏览多行评价，了解平台在真实场景中的使用反馈。</p>
        </div>

        <div v-if="testimonialsLoading" class="testimonials-state">加载评价中…</div>
        <div v-else-if="testimonialsError" class="testimonials-state">评价加载失败，已显示默认内容。</div>

        <div class="testimonials-marquee" role="list" aria-label="用户反馈卡片弹幕展示">
          <div class="lane lane--1" aria-label="评价泳道 1">
            <div class="track">
              <article v-for="t in laneLoops[0]" :key="`l1-${t.id}`" class="t-card" role="listitem">
                <div class="t-head">
                  <img class="t-avatar" :src="t.avatar" :alt="`${t.name} 头像`" />
                  <p class="t-name">{{ t.name }}</p>
                </div>
                <p class="t-text">{{ t.text }}</p>
              </article>
              <article v-for="t in laneLoops[0]" :key="`l1b-${t.id}`" class="t-card" role="listitem">
                <div class="t-head">
                  <img class="t-avatar" :src="t.avatar" :alt="`${t.name} 头像`" />
                  <p class="t-name">{{ t.name }}</p>
                </div>
                <p class="t-text">{{ t.text }}</p>
              </article>
            </div>
          </div>

          <div class="lane lane--2" aria-label="评价泳道 2">
            <div class="track">
              <article v-for="t in laneLoops[1]" :key="`l2-${t.id}`" class="t-card" role="listitem">
                <div class="t-head">
                  <img class="t-avatar" :src="t.avatar" :alt="`${t.name} 头像`" />
                  <p class="t-name">{{ t.name }}</p>
                </div>
                <p class="t-text">{{ t.text }}</p>
              </article>
              <article v-for="t in laneLoops[1]" :key="`l2b-${t.id}`" class="t-card" role="listitem">
                <div class="t-head">
                  <img class="t-avatar" :src="t.avatar" :alt="`${t.name} 头像`" />
                  <p class="t-name">{{ t.name }}</p>
                </div>
                <p class="t-text">{{ t.text }}</p>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section class="metrics">
        <h2 class="section-title">平台能力指标</h2>
        <div class="metrics-grid">
          <div class="metric-card">
            <p class="metric-value">120万+</p>
            <p class="metric-label">农资数据条目</p>
          </div>
          <div class="metric-card">
            <p class="metric-value">7 x 24</p>
            <p class="metric-label">动态更新机制</p>
          </div>
          <div class="metric-card">
            <p class="metric-value">3000+</p>
            <p class="metric-label">合作采购渠道</p>
          </div>
          <div class="metric-card">
            <p class="metric-value">秒级</p>
            <p class="metric-label">检索响应体验</p>
          </div>
        </div>
      </section>

      <footer class="site-footer" aria-label="网站页脚">
        <div class="footer-inner">
          <div class="footer-top">
            <div class="footer-brand">
              <p class="footer-logo">禾信综合农资平台</p>
              <p class="footer-desc">
                面向农业经营者、采购方与服务企业，提供可信的农资数据、行情洞察与渠道连接能力。
              </p>
              <p class="footer-welcome">欢迎你，{{ username || '访客' }}。</p>
            </div>

            <div class="footer-cols">
              <div class="footer-col">
                <p class="footer-title">产品与支持</p>
                <div class="footer-links-grid">
                  <a class="footer-link" href="#gallery">数据与渠道展示</a>
                  <a class="footer-link" href="#pesticide">农药信息库</a>
                  <a class="footer-link" href="#testimonials">用户评价</a>
                  <a class="footer-link" href="#" @click.prevent>使用指南</a>
                  <a class="footer-link" href="#" @click.prevent>API 文档</a>
                  <a class="footer-link" href="#" @click.prevent>常见问题</a>
                </div>
              </div>
              <div class="footer-col">
                <p class="footer-title">联系我们</p>
                <p class="footer-item"><span class="k">邮箱</span><span class="v">1185902279@qq.com</span></p>
                <p class="footer-item"><span class="k">电话</span><span class="v">18962901710</span></p>
                <p class="footer-item"><span class="k">地址</span><span class="v">江苏省徐州市铜山区中国矿业大学徐海学院</span></p>
              </div>
            </div>

          </div>

          <div class="footer-bottom">
            <div class="footer-social" aria-label="社交媒体">
              <a class="social-link" href="#" @click.prevent aria-label="TikTok" title="TikTok">
                <img class="social-svg" src="/icons/tiktok.svg" alt="" aria-hidden="true" />
              </a>
              <a class="social-link" href="#" @click.prevent aria-label="WeChat" title="WeChat">
                <img class="social-svg" src="/icons/wechat.svg" alt="" aria-hidden="true" />
              </a>
              <a class="social-link" href="#" @click.prevent aria-label="X" title="X">
                <img class="social-svg" src="/icons/x.svg" alt="" aria-hidden="true" />
              </a>
              <a class="social-link" href="#" @click.prevent aria-label="YouTube" title="YouTube">
                <img class="social-svg" src="/icons/youtube.svg" alt="" aria-hidden="true" />
              </a>
              <a class="social-link" href="#" @click.prevent aria-label="Bilibili" title="Bilibili">
                <img class="social-svg" src="/icons/bilibili.svg" alt="" aria-hidden="true" />
              </a>
            </div>
            <p class="footer-copy">© {{ new Date().getFullYear() }} 禾信综合农资平台 · All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  </div>
</template>

<script>
import HmButton from './common/HmButton.vue'
import lightbulbIcon from '../assets/lightbulb-pixel.svg'
import eyeOpenIcon from '../assets/eye-open.svg'

export default {
  name: 'HomeComponent',
  components: { HmButton },
  props: {
    username: {
      type: String,
      default: ''
    },
    isLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      lightbulbIcon,
      eyeOpenIcon,
        slideDir: 1,
      testimonials: [],
      testimonialsLoading: true,
      testimonialsError: false,
      testimonialsLaneCount: 2,
      currentSlide: 0,
      slideTimer: null,
      galleryCards: [],
      pesticides: [],
      heroSlides: [
        {
          id: 's1',
          image: '',
          kicker: '农业数据基础设施',
          title: '收集海量农资信息，让查找与采购更高效',
          text: '按品类、地区、时段快速筛选，秒级定位所需农资数据。'
        },
        {
          id: 's2',
          image: '',
          kicker: '市场与趋势分析',
          title: '行情洞察面板，辅助采购决策',
          text: '聚合价格与供需变化趋势，支持采购策略调整。'
        },
        {
          id: 's3',
          image: '',
          kicker: '风控与合规管理',
          title: '资质核验与渠道评分联动',
          text: '资质核验与渠道评分联动，降低交易中的不确定风险。'
        }
      ]
    }
  },
  created() {
    this.loadHeroSlides()
    this.loadGalleryCards()
    this.loadPesticides()
    this.loadTestimonials()
  },
  mounted() {
    this.startSlideAutoPlay()
  },
  beforeDestroy() {
    this.stopSlideAutoPlay()
  },
  computed: {
    laneLoops() {
      const lanes = Array.from({ length: this.testimonialsLaneCount }, () => [])
      const src = Array.isArray(this.testimonials) ? this.testimonials : []
      for (let i = 0; i < src.length; i += 1) {
        lanes[i % this.testimonialsLaneCount].push(src[i])
      }
      // 保底：数据不足时复制，避免某条泳道为空导致动画突兀
      return lanes.map((lane) => {
        if (lane.length === 0) return []
        if (lane.length >= 4) return lane
        const out = lane.slice()
        while (out.length < 4) out.push(...lane)
        return out.slice(0, 6)
      })
    }
  },
  methods: {
    handleMorePesticides() {
      this.$emit('more-pesticides')
    },
    async loadPesticides() {
      const fallback = [
        {
          id: 'p1',
          image: '/img/003.jpeg',
          name: '吡虫啉',
          enName: 'Imidacloprid',
          type: '杀虫剂',
          summary: '适用于蚜虫、粉虱、叶蝉等刺吸式害虫防治，见效快、持效期较长。',
          targets: '蚜虫 / 粉虱 / 叶蝉等刺吸式害虫',
          crops: '蔬菜 / 果树 / 经济作物',
          usage: '按标签推荐浓度配药，均匀喷雾；尽量避开高温强光时段。',
          notes: '轮换用药降低抗性风险；远离蜂群与水体；按安全间隔期采收。'
        },
        {
          id: 'p2',
          image: '/img/004.jpeg',
          name: '多菌灵',
          enName: 'Carbendazim',
          type: '杀菌剂',
          summary: '对多种真菌性病害有防治作用，可用于白粉病、炭疽病等的预防与控制。',
          targets: '白粉病 / 炭疽病 / 叶斑病等真菌性病害',
          crops: '粮食作物 / 蔬菜 / 果树',
          usage: '以预防为主，发病初期或雨后及时补喷；注意覆盖叶背等部位。',
          notes: '避免长期单一使用；与不同机制药剂轮换；严格遵守安全间隔期。'
        }
      ]

      try {
        const res = await fetch('/pesticides.json', { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.pesticides = Array.isArray(data) && data.length ? data : fallback
      } catch (e) {
        this.pesticides = fallback
      }
    },
    async loadGalleryCards() {
      const fallback = [
        {
          id: 'g1',
          image: '/img/003.jpeg',
          status: '实时检索中',
          title: '农资数据检索',
          text: '多维筛选与关键词检索并行，快速定位目标农资信息。'
        },
        {
          id: 'g2',
          image: '/img/004.jpeg',
          status: '洞察分析面板',
          title: '行情洞察与趋势',
          text: '按区域、品类、周期聚合变化趋势，辅助采购判断。'
        },
        {
          id: 'g3',
          image: '/img/003.jpeg',
          status: '风控规则已启用',
          title: '合规与风控',
          text: '供应资质、渠道稳定性、批次信息交叉校验，降低交易风险。'
        }
      ]

      try {
        const res = await fetch('/gallery-cards.json', { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.galleryCards = Array.isArray(data) && data.length ? data : fallback
      } catch (e) {
        this.galleryCards = fallback
      }
    },
    async loadHeroSlides() {
      const fallback = [
        {
          id: 's1',
          image: '',
          kicker: '农业数据基础设施',
          title: '收集海量农资信息，让查找与采购更高效',
          text: '按品类、地区、时段快速筛选，秒级定位所需农资数据。'
        },
        {
          id: 's2',
          image: '',
          kicker: '市场与趋势分析',
          title: '行情洞察面板，辅助采购决策',
          text: '聚合价格与供需变化趋势，支持采购策略调整。'
        },
        {
          id: 's3',
          image: '',
          kicker: '风控与合规管理',
          title: '资质核验与渠道评分联动',
          text: '资质核验与渠道评分联动，降低交易中的不确定风险。'
        }
      ]

      try {
        const res = await fetch('/hero-slides.json', { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.heroSlides = Array.isArray(data) && data.length ? data : fallback
      } catch (e) {
        this.heroSlides = fallback
      } finally {
        if (this.currentSlide >= this.heroSlides.length) {
          this.currentSlide = 0
        }
      }
    },
    startSlideAutoPlay() {
      this.stopSlideAutoPlay()
      this.slideTimer = setInterval(() => {
        this.nextSlide()
      }, 3500)
    },
    stopSlideAutoPlay() {
      if (this.slideTimer) {
        clearInterval(this.slideTimer)
        this.slideTimer = null
      }
    },
    nextSlide() {
      this.slideDir = 1
      this.currentSlide = (this.currentSlide + 1) % this.heroSlides.length
      this.startSlideAutoPlay()
    },
    prevSlide() {
      this.slideDir = -1
      this.currentSlide = (this.currentSlide - 1 + this.heroSlides.length) % this.heroSlides.length
      this.startSlideAutoPlay()
    },
    goToSlide(idx) {
      const oldIdx = this.currentSlide
      this.slideDir = idx >= oldIdx ? 1 : -1
      this.currentSlide = idx
      this.startSlideAutoPlay()
    },
    async loadTestimonials() {
      const fallback = [
        {
          id: 'fallback-001',
          avatar: this.lightbulbIcon,
          name: '访客用户',
          text: '页面清晰易用，像素风很有辨识度，信息重点突出。'
        },
        {
          id: 'fallback-002',
          avatar: this.eyeOpenIcon,
          name: '采购专员',
          text: '卡片式展示直观，滚动浏览很顺手，适合快速对比与决策。'
        }
      ]

      this.testimonialsLoading = true
      this.testimonialsError = false
      try {
        const res = await fetch('/testimonials.json', { cache: 'no-store' })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.testimonials = Array.isArray(data) && data.length ? data : fallback
        if (!Array.isArray(data) || !data.length) this.testimonialsError = true
      } catch (e) {
        this.testimonials = fallback
        this.testimonialsError = true
      } finally {
        this.testimonialsLoading = false
      }
    },
    // 交互由 CSS 弹幕动画控制；JS 只负责数据加载
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home-page {
  --panel: rgba(23, 28, 40, 0.9);
  --panel-soft: rgba(30, 36, 50, 0.9);
  --line: #3f2f1f;
  --accent: #ffd46a;
  --text: #f7e5be;
  --muted: #b8a98f;
  min-height: 100vh;
  background:
    linear-gradient(rgba(9, 11, 18, 0.58), rgba(9, 11, 18, 0.58)),
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  font-family: 'Courier New', 'Lucida Console', monospace;
  color: var(--text);
  image-rendering: pixelated;
}

.home-main {
  width: min(1180px, 94%);
  margin: 0 auto;
  padding: 26px 0 56px;
}

.hero {
  border: 2px solid var(--line);
  background: var(--panel);
  padding: 24px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 8px 0 rgba(8, 10, 15, 0.42);
}

.hero-carousel-full {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.hero-slide-stage {
  position: relative;
  overflow: hidden;
  border: 2px solid #65462a;
  box-shadow: 0 4px 0 #1a2230;
}

.hero-slide-media {
  background: #1f2734;
  height: clamp(340px, 52vh, 440px);
  max-height: 440px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-slide-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  backface-visibility: hidden;
}

/* 像素风淡入：用 steps 避免“顺滑糊掉”，同时让切换不那么生硬 */
.hero-slide-media-enter-active,
.hero-slide-media-leave-active {
  transition: opacity 160ms linear, transform 260ms ease;
  will-change: opacity, transform;
}
.hero-slide-media-enter-from {
  opacity: 0;
  transform: translateX(calc(var(--slide-dir) * 22px));
}
.hero-slide-media-leave-to {
  opacity: 0;
  transform: translateX(calc(var(--slide-dir) * -22px));
}

.hero-slide-text-enter-active,
.hero-slide-text-leave-active {
  transition: opacity 160ms linear, transform 240ms ease;
  will-change: opacity, transform;
}
.hero-slide-text-enter-from {
  opacity: 0;
  transform: translateX(calc(var(--slide-dir) * 14px));
}

.hero-slide-text-leave-to {
  opacity: 0;
  transform: translateX(calc(var(--slide-dir) * -14px));
}

.hero-slide-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    #1d2431;
  background-size: 8px 8px, 8px 8px, auto;
  color: #d8b77a;
  letter-spacing: 1px;
  font-size: 12px;
  text-align: center;
  padding: 20px;
}

.placeholder-badge {
  font-size: 11px;
  color: #1f160e;
  background: #ffd46a;
  border: 1px solid #6c4d26;
  padding: 4px 8px;
}

.placeholder-title {
  margin-top: 14px;
  font-size: 32px;
  line-height: 1.45;
  max-width: 760px;
  color: #ffe9bc;
  text-shadow: 2px 2px 0 #2a1b10;
}

.placeholder-tip {
  margin-top: 10px;
  font-size: 12px;
  color: #cab998;
}

.hero-slide-info {
  padding: 16px;
}

.hero-slide-info--overlay {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(9, 11, 18, 0) 0%, rgba(9, 11, 18, 0.88) 50%, rgba(9, 11, 18, 0.95) 100%);
}

.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: var(--accent);
  background: rgba(255, 212, 106, 0.1);
  border: 1px solid rgba(255, 212, 106, 0.3);
  width: fit-content;
  padding: 6px 10px;
}

.hero-tag-dot {
  width: 6px;
  height: 6px;
  background: #ffd46a;
  box-shadow: 0 0 0 1px #6c4d26;
}

.hero-title {
  margin-top: 16px;
  font-size: 52px;
  line-height: 1.35;
  letter-spacing: 1px;
  font-weight: 700;
  color: #fff2d2;
  text-shadow: 2px 2px 0 #2b1d12;
}

.hero-desc {
  margin-top: 18px;
  max-width: 720px;
  font-size: 14px;
  line-height: 1.8;
  color: #dacdb8;
}

.hero-slide-controls {
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.hero-quick-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.quick-item {
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 3px 0 #1a2230;
  padding: 10px 12px;
}

.quick-k {
  font-size: 11px;
  color: #d8b77a;
  letter-spacing: 1px;
}

.quick-v {
  margin-top: 6px;
  font-size: 16px;
  font-weight: 700;
  color: #ffe5a8;
}

.carousel-nav {
  width: 40px;
  height: 36px;
  border: 2px solid #4f3a24;
  background: #2f384a;
  color: #ffe5a8;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 4px 0 #1b2230;
}

.carousel-nav:hover {
  filter: brightness(1.1);
}

.carousel-nav:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #1b2230;
}

.carousel-dots {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border: 1px solid #6c4d26;
  background: #2b3343;
  cursor: pointer;
}

.dot.active {
  background: #ffd46a;
}

.gallery {
  margin-top: 24px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 24px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.showcase-card {
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 4px 0 #1a2230;
  padding: 12px;
  transition: transform 0.12s ease, border-color 0.12s ease;
}

.showcase-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 212, 106, 0.45);
}

.showcase-top {
  display: flex;
  align-items: center;
  gap: 6px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(101, 70, 42, 0.65);
}

.showcase-dot {
  width: 8px;
  height: 8px;
  background: #7d5a35;
  box-shadow: 0 0 0 1px #3e2a16;
}

.showcase-status {
  margin-left: auto;
  font-size: 11px;
  color: #d8b77a;
  letter-spacing: 1px;
}

.showcase-screen {
  margin-top: 10px;
  min-height: 120px;
  border: 2px solid #3d2b1b;
  background:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    #1d2431;
  background-size: 8px 8px, 8px 8px, auto;
  padding: 0;
  overflow: hidden;
}

.showcase-card--search .showcase-screen {
  background-color: #1f2735;
}

.showcase-card--insight .showcase-screen {
  background-color: #232a36;
}

.showcase-card--risk .showcase-screen {
  background-color: #222833;
}

.showcase-img {
  width: 100%;
  height: 140px;
  display: block;
  object-fit: cover;
  image-rendering: pixelated;
  filter: saturate(0.95) contrast(1.05);
}

.screen-line {
  display: block;
  height: 10px;
  margin-bottom: 10px;
  background: linear-gradient(90deg, rgba(255, 212, 106, 0.7), rgba(255, 212, 106, 0.2));
}

.w-90 {
  width: 90%;
}

.w-72 {
  width: 72%;
}

.w-56 {
  width: 56%;
}

.screen-bars {
  height: 96px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.bar {
  width: 18px;
  background: linear-gradient(180deg, #ffd46a, #8b652f);
  border: 1px solid #5b3f1d;
}

.h-62 {
  height: 62%;
}

.h-38 {
  height: 38%;
}

.h-74 {
  height: 74%;
}

.h-48 {
  height: 48%;
}

.h-66 {
  height: 66%;
}

.screen-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  font-size: 11px;
  color: #1f160e;
  font-weight: 700;
  letter-spacing: 0.5px;
  background: #ffd46a;
  border: 1px solid #6c4d26;
  padding: 5px 8px;
}

.showcase-title {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
}

.showcase-text {
  margin-top: 8px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--muted);
}

.pesticide {
  margin-top: 24px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 24px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.pesticide-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.pesticide-card {
  border: 2px solid #65462a;
  background: #2b3343;
  box-shadow: 0 4px 0 #1a2230;
  padding: 12px;
}

.pesticide-media {
  border: 2px solid #3d2b1b;
  background:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    #1d2431;
  background-size: 8px 8px, 8px 8px, auto;
  overflow: hidden;
  margin-bottom: 10px;
}

.pesticide-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  height: auto;
  display: block;
  object-fit: contain;
  object-position: center;
  image-rendering: pixelated;
  filter: saturate(0.95) contrast(1.05);
  background:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 8px 8px, 8px 8px;
}

.pesticide-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(101, 70, 42, 0.7);
}

.pesticide-name {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
}

.pesticide-en {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: rgba(213, 174, 99, 0.95);
}

.pesticide-badge {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #2b1d12;
  background: #ffd46a;
  border: 2px solid #6c4d26;
  padding: 4px 8px;
}

.pesticide-desc {
  margin-top: 10px;
  font-size: 12px;
  line-height: 1.75;
  color: var(--muted);
}

.pesticide-meta {
  margin-top: 10px;
  display: grid;
  gap: 8px;
}

.pesticide-meta li {
  display: flex;
  gap: 10px;
  align-items: baseline;
}

.pesticide-meta .k {
  flex: 0 0 44px;
  color: #d5ae63;
  font-weight: 700;
  letter-spacing: 1px;
}

.pesticide-meta .v {
  color: #cbbca2;
  line-height: 1.6;
}

.testimonials {
  margin-top: 24px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 24px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.testimonials-head {
  text-align: center;
  padding: 6px 0 10px;
}

.testimonials-kicker {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
}

.testimonials-title {
  margin-top: 10px;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
  text-shadow: 2px 2px 0 #2a1b10;
}

.testimonials-subtitle {
  margin-top: 10px;
  font-size: 12px;
  line-height: 1.7;
  letter-spacing: 0.5px;
  color: var(--muted);
}

.testimonials-state {
  margin-top: 14px;
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 1px;
  text-align: center;
}

.testimonials-marquee {
  margin-top: 14px;
  position: relative;
  border: 2px solid rgba(101, 70, 42, 0.55);
  background: rgba(0, 0, 0, 0.1);
  padding: 12px clamp(12px, 4vw, 36px);
  overflow: hidden;
  -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 10%, #000 90%, transparent 100%);
  mask-image: linear-gradient(180deg, transparent 0%, #000 10%, #000 90%, transparent 100%);
}

.lane {
  overflow: hidden;
  padding: 8px 0;
}

.lane--1 {
  --marquee-offset: 0px;
}

.lane--2 {
  --marquee-offset: -180px;
}

.track {
  display: inline-flex;
  gap: 12px;
  will-change: transform;
  animation: marquee-left 36s linear infinite;
}

.lane--2 .track {
  /* 两行同速 */
  animation-duration: 36s;
  animation-delay: 0s;
}

.lane:hover .track {
  animation-play-state: paused;
}

@keyframes marquee-left {
  from {
    transform: translateX(var(--marquee-offset, 0px));
  }
  to {
    transform: translateX(calc(-50% + var(--marquee-offset, 0px)));
  }
}

@media (prefers-reduced-motion: reduce) {
  .track {
    animation: none;
  }
  .testimonials-marquee {
    overflow: auto;
  }
}

.t-card {
  scroll-snap-align: start;
  border: 2px solid #65462a;
  background: rgba(18, 22, 30, 0.85);
  box-shadow: 0 4px 0 #1a2230;
  padding: 14px 14px 16px;
  width: 320px;
  flex: 0 0 auto;
  transition: transform 0.12s ease, filter 0.12s ease, border-color 0.12s ease;
}

.t-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 212, 106, 0.45);
  filter: brightness(1.06);
}

.t-head {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(101, 70, 42, 0.7);
}

.t-avatar {
  width: 34px;
  height: 34px;
  border: 2px solid #3d2b1b;
  background: #252c3a;
  image-rendering: pixelated;
  border-radius: 999px;
}

.t-name {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
}

.t-text {
  margin-top: 12px;
  font-size: 12px;
  line-height: 1.75;
  color: #cbbca2;
  letter-spacing: 0.5px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--line);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 70px;
  height: 2px;
  background: var(--accent);
}

.more-btn {
  display: inline-block;
}

.pesticide-more {
  margin-top: 14px;
  display: flex;
  justify-content: center;
}

.more-btn /deep/ .retro-btn__frame {
  width: 132px;
  height: 40px;
}

.more-btn /deep/ .retro-btn__label {
  font-size: 11px;
  letter-spacing: 1px;
}

.metrics,
.final-cta {
  margin-top: 24px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 24px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.metric-card {
  border: 2px solid #4e3a24;
  background: #2d3445;
  padding: 14px;
  text-align: center;
  box-shadow: 0 4px 0 #1b2230;
}

.metric-value {
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffd46a;
  text-shadow: 2px 2px 0 #332310;
}

.metric-label {
  margin-top: 8px;
  font-size: 12px;
  color: var(--muted);
}

.site-footer {
  margin-top: 24px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 54px 44px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.footer-inner {
  background: rgba(18, 22, 30, 0.72);
  border: 2px solid rgba(101, 70, 42, 0.65);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.06);
  padding: 34px 28px;
}

.footer-top {
  display: grid;
  grid-template-columns: 1.2fr 2.8fr;
  gap: 28px;
  align-items: start;
}

.footer-brand {
  padding-right: 10px;
}

.footer-logo {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #ffe5a8;
}

.footer-desc {
  margin-top: 12px;
  font-size: 14px;
  line-height: 1.85;
  color: var(--muted);
}

.footer-welcome {
  margin-top: 10px;
  font-size: 13px;
  color: #d5ae63;
  letter-spacing: 0.5px;
}

.footer-cols {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 26px;
}

.footer-col {
  padding: 6px 0 0;
}

.footer-title {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #ffe5a8;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(101, 70, 42, 0.7);
}

.footer-link {
  display: block;
  margin-top: 12px;
  font-size: 14px;
  color: #cbbca2;
  letter-spacing: 0.5px;
  text-decoration: none;
}

.footer-links-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 22px;
}

.footer-links-grid .footer-link {
  margin-top: 12px;
}

.footer-link.inline {
  display: inline;
  margin-top: 0;
}

.footer-link:hover {
  color: #ffe8b0;
}

.footer-item {
  margin-top: 12px;
  display: flex;
  gap: 10px;
  font-size: 14px;
  line-height: 1.7;
  color: #cbbca2;
}

.footer-item .k {
  flex: 0 0 34px;
  color: #d5ae63;
  font-weight: 700;
  letter-spacing: 1px;
}

.footer-item .v {
  color: #cbbca2;
}

.footer-bottom {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px solid rgba(101, 70, 42, 0.7);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.footer-copy {
  font-size: 14px;
  color: var(--muted);
  letter-spacing: 0.5px;
}

.footer-social {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.social-link {
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 4px 0 #1a2230;
  text-decoration: none;
  color: #ffe5a8;
}

.social-link:hover {
  filter: brightness(1.08);
}

.social-link:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #1a2230;
}

.social-svg {
  width: 20px;
  height: 20px;
  display: block;
  /* 外部 svg 通过文件内填充色显示；亮色模式下压暗以增强对比 */
  filter: none;
}


.home-page.light-mode {
  --panel: rgba(255, 249, 238, 0.9);
  --panel-soft: rgba(250, 242, 230, 0.92);
  --line: #9a7348;
  --accent: #a86820;
  --text: #3f2c1f;
  --muted: #564636;
  background:
    linear-gradient(rgba(255, 248, 236, 0), rgba(255, 248, 236, 0)),
    linear-gradient(rgba(66, 49, 32, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(66, 49, 32, 0.07) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  color: var(--text);
}

.home-page.light-mode .hero-tag {
  color: #8b5a1e;
  background: rgba(168, 104, 32, 0.12);
  border-color: rgba(154, 115, 72, 0.45);
}

.home-page.light-mode .hero-desc,
.home-page.light-mode .feature-text,
.home-page.light-mode .showcase-text,
.home-page.light-mode .pesticide-desc,
.home-page.light-mode .cta-subtitle,
.home-page.light-mode .metric-label,
.home-page.light-mode .testimonials-subtitle,
.home-page.light-mode .testimonials-hint,
.home-page.light-mode .t-text {
  color: #4f4032;
}

.home-page.light-mode .showcase-status,
.home-page.light-mode .quick-k {
  color: #6a4a2a;
}

.home-page.light-mode .pesticide-meta .v {
  color: #4f4032;
}

.home-page.light-mode .hero-slide-info--overlay .hero-title,
.home-page.light-mode .hero-slide-info--overlay .hero-desc {
  color: #2f2117;
}

.home-page.light-mode .hero-slide-info--overlay .hero-title {
  text-shadow: none;
}

.home-page.light-mode .site-header {
  background: rgba(252, 246, 235, 0.9);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.72), 0 6px 0 rgba(135, 100, 62, 0.18);
}

.home-page.light-mode .brand-logo {
  border-color: rgba(154, 115, 72, 0.85);
  background: #f8f0e2;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.62), 0 4px 0 rgba(138, 100, 64, 0.12);
}

.home-page.light-mode .brand-cn {
  color: #694322;
  text-shadow: 2px 2px 0 rgba(255, 240, 214, 0.75);
}

.home-page.light-mode .hero-title,
.home-page.light-mode .feature-title {
  color: #5f3c1e;
  text-shadow: none;
}

.home-page.light-mode .showcase-card,
.home-page.light-mode .pesticide-card {
  background: #f8f0e2;
  border-color: #9a7348;
  box-shadow: 0 4px 0 rgba(138, 100, 64, 0.24);
}

.home-page.light-mode .metrics {
  background: var(--panel-soft);
  border-color: #9a7348;
}

.home-page.light-mode .metric-card {
  background: #f8f0e2;
  border-color: #9a7348;
  box-shadow: 0 4px 0 rgba(138, 100, 64, 0.18);
}

.home-page.light-mode .footer-brand,
.home-page.light-mode .footer-col {
  background: transparent;
  border-color: transparent;
  box-shadow: none;
}

.home-page.light-mode .footer-inner {
  background: rgba(255, 252, 246, 0.75);
  border-color: rgba(154, 115, 72, 0.55);
}

.home-page.light-mode .footer-logo,
.home-page.light-mode .footer-title {
  color: #5f3c1e;
}

.home-page.light-mode .footer-desc,
.home-page.light-mode .footer-copy,
.home-page.light-mode .footer-link,
.home-page.light-mode .footer-item,
.home-page.light-mode .footer-item .v {
  color: #4f4032;
}

.home-page.light-mode .footer-item .k,
.home-page.light-mode .footer-welcome {
  color: #6a4a2a;
}

.home-page.light-mode .footer-link:hover {
  color: #2f2117;
}

.home-page.light-mode .footer-bottom {
  border-top-color: rgba(154, 115, 72, 0.55);
}

.home-page.light-mode .social-link {
  background: #f8f0e2;
  border-color: #9a7348;
  box-shadow: 0 4px 0 rgba(138, 100, 64, 0.18);
  color: #5f3c1e;
}

.home-page.light-mode .social-svg {
  filter: brightness(0.45) saturate(120%);
}

.home-page.light-mode .pesticide-media {
  border-color: rgba(154, 115, 72, 0.7);
  background:
    linear-gradient(rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    #fbf3e7;
  background-size: 8px 8px, 8px 8px, auto;
}

.home-page.light-mode .pesticide-en {
  color: rgba(106, 74, 42, 0.9);
}

.home-page.light-mode .hero-slide-media,
.home-page.light-mode .hero-slide-placeholder {
  border-color: rgba(154, 115, 72, 0.72);
  background:
    linear-gradient(rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    #fbf3e7;
  background-size: 8px 8px, 8px 8px, auto;
}

.home-page.light-mode .hero-slide-info--overlay {
  background: linear-gradient(180deg, rgba(255, 250, 240, 0) 0%, rgba(255, 250, 240, 0.8) 50%, rgba(255, 250, 240, 0.93) 100%);
}

.home-page.light-mode .placeholder-badge {
  color: #fff7ea;
  background: #9d621f;
  border-color: #744516;
}

.home-page.light-mode .placeholder-title {
  color: #5f3c1e;
  text-shadow: 2px 2px 0 rgba(255, 240, 214, 0.75);
}

.home-page.light-mode .placeholder-tip {
  color: #705a46;
}

.home-page.light-mode .quick-item {
  background: #efe2cd;
  border-color: #8a6440;
  box-shadow: 0 3px 0 rgba(138, 100, 64, 0.35);
}

.home-page.light-mode .quick-k {
  color: #8b5f2e;
}

.home-page.light-mode .quick-v {
  color: #5f3c1e;
}

.home-page.light-mode .carousel-nav {
  background: #e9d8bf;
  color: #5f3c1e;
  border-color: rgba(154, 115, 72, 0.65);
  box-shadow: 0 4px 0 #c4a37f;
}

.home-page.light-mode .metric-value {
  color: #9d621f;
  text-shadow: none;
}

.home-page.light-mode .metric-label {
  color: #4f4032;
}

.home-page.light-mode .showcase-screen {
  border-color: rgba(154, 115, 72, 0.7);
  background:
    linear-gradient(rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(58, 41, 25, 0.07) 1px, transparent 1px),
    #fbf3e7;
  background-size: 8px 8px, 8px 8px, auto;
}

.home-page.light-mode .showcase-title,
.home-page.light-mode .pesticide-name {
  color: #5f3c1e;
}

.home-page.light-mode .showcase-status {
  color: #8b5f2e;
}

.home-page.light-mode .screen-line {
  background: linear-gradient(90deg, rgba(157, 98, 31, 0.75), rgba(157, 98, 31, 0.2));
}

.home-page.light-mode .bar {
  background: linear-gradient(180deg, #b77a35, #7c4d1b);
  border-color: #8a5d2c;
}

.home-page.light-mode .pesticide-badge {
  color: #fff7ea;
  background: #9d621f;
  border-color: #744516;
}

.home-page.light-mode .pesticide-meta .v {
  color: #5d4f43;
}

.home-page.light-mode .testimonials {
  background: var(--panel-soft);
}

.home-page.light-mode .testimonials-title {
  color: #5f3c1e;
  text-shadow: 2px 2px 0 rgba(255, 240, 214, 0.75);
}

.home-page.light-mode .testimonials-marquee {
  border-color: rgba(154, 115, 72, 0.55);
  background: rgba(255, 252, 246, 0.58);
}

.home-page.light-mode .testimonials-hint {
  color: var(--muted);
  border-color: rgba(138, 100, 64, 0.55);
  background: rgba(255, 255, 255, 0.35);
}

.home-page.light-mode .t-card {
  background: rgba(253, 248, 240, 0.95);
  border-color: #9a7348;
  box-shadow: 0 4px 0 rgba(138, 100, 64, 0.24);
}

.home-page.light-mode .t-head {
  border-bottom-color: rgba(138, 100, 64, 0.55);
}

.home-page.light-mode .t-avatar {
  border-color: rgba(138, 100, 64, 0.75);
  background: rgba(255, 255, 255, 0.2);
}

.home-page.light-mode .t-name {
  color: #5f3c1e;
}

.home-page.light-mode .t-text {
  color: #5d4f43;
}

.home-page.light-mode .theme-toggle {
  color: #5f3c1e;
}

.home-page.light-mode .login-corner-btn {
  color: #5f3c1e;
}

.home-page.light-mode .theme-toggle /deep/ .retro-btn__frame,
.home-page.light-mode .login-corner-btn /deep/ .retro-btn__frame {
  background: linear-gradient(160deg, #d3b58e, #9a7348);
}

.home-page.light-mode .theme-toggle /deep/ .retro-btn__inner,
.home-page.light-mode .login-corner-btn /deep/ .retro-btn__inner {
  background: linear-gradient(180deg, #e3cca8 0%, #b28658 100%);
}

.home-page.light-mode .theme-toggle.on {
  color: #8f4f00;
}

@media (max-width: 1100px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }

  .pesticide-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .capability-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 920px) {
  .site-header {
    padding: 0 18px;
  }

  .hero {
    padding: 26px 20px;
  }

  .hero-slide-media,
  .hero-slide-img,
  .hero-slide-placeholder {
    height: 300px;
    max-height: 300px;
  }

  /* 移动端：缩小轮播图内文字，避免拥挤遮挡 */
  .hero-tag {
    font-size: 10px;
    letter-spacing: 1px;
    padding: 5px 8px;
  }

  .hero-title {
    font-size: 30px;
    line-height: 1.25;
  }

  .hero-desc {
    font-size: 12px;
    line-height: 1.7;
    max-width: 520px;
  }

  .pesticide-grid {
    grid-template-columns: 1fr;
  }

  .hero-quick-grid {
    grid-template-columns: 1fr;
  }

  .testimonials-marquee {
    padding: 10px;
  }

  .t-card {
    width: 260px;
  }

  .metrics-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .footer-top {
    grid-template-columns: 1fr;
  }

  .footer-cols {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
  }

  .footer-links-grid {
    grid-template-columns: 1fr;
    column-gap: 0;
  }

  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
  }

  .site-footer {
    padding: 36px 20px;
  }

  .footer-inner {
    padding: 24px 16px;
  }

  .footer-media-slot {
    max-width: 280px;
  }
}

@media (max-width: 680px) {
  /* 更小屏：再收一点字号 */
  .hero-title {
    font-size: 24px;
  }

  .hero-desc {
    font-size: 11px;
  }
}
</style>
