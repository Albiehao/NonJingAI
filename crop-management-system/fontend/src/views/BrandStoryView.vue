<template>
  <div class="story-page" :class="{ 'light-mode': globalLightMode }">
    <main class="story-main">
      <section class="story-hero">
        <div class="hero-bg" :style="{ backgroundImage: `url(${heroImage})` }" aria-hidden="true"></div>
        <div class="hero-overlay" aria-hidden="true"></div>
        <div class="hero-grid" aria-hidden="true"></div>

        <div class="hero-content">
          <div class="hero-left">
            <p class="kicker">BRAND STORY</p>
            <h1 class="title">把星露谷的“温柔秩序”，带回传统农业的每一次选择</h1>
            <p class="subtitle">
              我们喜欢《星露谷物语》的原因很简单：它把复杂的农事拆成了可以理解、可以计划、可以复盘的小步骤。
              现实农业更真实也更艰难——但“清晰的信息 + 合适的工具 + 可靠的服务”，同样能让你更安心。
            </p>
            <div class="chips" aria-label="关键词">
              <span class="chip">像素田园</span>
              <span class="chip">传统经验</span>
              <span class="chip">可信供应</span>
              <span class="chip">明码透明</span>
            </div>
          </div>
        </div>
      </section>

      <article class="story-article">
        <header class="article-head">
          <p class="article-meta">
            <span class="meta-pill">平台介绍</span>
            <span class="meta-dot" aria-hidden="true">·</span>
            <time :datetime="publishedAtISO">{{ publishedAtText }}</time>
            <span class="meta-dot" aria-hidden="true">·</span>
            <span>阅读约 3 分钟</span>
          </p>
          <h2 class="article-title">品牌故事</h2>
          <p class="article-lead">
            我们用星露谷式的“可理解、可计划、可复盘”做体验，用传统农业的“因地制宜、敬畏规律”做底层方法。
            这两者的交集，是一件事：把不确定性降到最低。
          </p>
        </header>

        <div class="prose">
          <h3>为什么我们会喜欢星露谷</h3>
          <p>
            在星露谷里，你不会被信息淹没：种子写清楚季节、天数与收获；工具有明确用途；村民的需求可以追踪。
            它不是“变简单”，而是把复杂拆得更可操作。
          </p>
          <p>
            更重要的是，它让你建立一种确定感：今天该做什么、这周该准备什么、这个季节该投入什么。每一次行动都能被解释，
            每一次投入都能被复盘——这正是现实农业里最稀缺、也最值钱的能力。
          </p>

          <blockquote>
            “慢一点、认真一点”不是口号，而是把每一步做对：选对作物、看对时机、用对产品、做对记录。
          </blockquote>

          <h3>传统农业教会我们的事</h3>
          <p>
            现实中，土壤、天气、病虫草害阶段、作物生育期都会影响结果。经验很宝贵，但经验也需要被表达得更清楚：
            成分是什么、适用什么、怎么用、什么时候不该用——这些本该是每次采购前就能看明白的内容。
          </p>
          <p>
            同样一款产品，放在不同土壤质地、不同降雨频次、不同作物时期，结果可能完全不同。我们尊重这种差异，
            所以更愿意把“适用边界”讲清楚：什么情况更合适，什么情况要谨慎，什么情况建议换思路。
          </p>

          <h3>我们希望你在平台上获得的体验</h3>
          <p>
            不是“看很多商品”，而是“更快做出判断”。你打开商品中心，像打开背包一样：分类清楚、目标明确、对比顺手。
            你不需要记住大量术语，只需要找到与你场景匹配的那一类，然后在可控范围内做选择。
          </p>
          <p>
            星露谷把农事拆成了可执行的小任务，我们也把采购拆成了更可执行的步骤：先确认作物与问题，再确认阶段与约束，
            最后在价格、规格与品牌之间做取舍。这样你会更踏实，因为每一步都有依据。
          </p>

          <h3>我们做平台，不只是“上架商品”</h3>
          <p>
            我们把关键字段做成更易读的结构，把商品中心做成更顺手的筛选与对比，把信息的“确认成本”降下来。
            你不需要凭运气试错，更像是在整理背包：每一件物品都知道自己要去哪里、什么时候用、为什么要用它。
          </p>
          <p>
            现实里常见的痛点，是信息分散与表达不一致：同类产品写法不同、重点藏在长段落里、禁忌与限制被忽略。
            我们更愿意做“统一表达”：让你在不同商品之间横向对比时，看的永远是同一套关键维度。
          </p>

          <h3>选品与信息的基本原则</h3>
          <p>
            你购买的不只是“一个名字”，而是一整套可依赖的信息。我们在呈现上坚持几件事：关键字段优先、描述避免含糊、
            对可能的误用给出提醒，并尽量让同类产品有可比性。
          </p>
          <ul>
            <li>先讲边界：适用与不适用要同时出现。</li>
            <li>先讲方法：用量、阶段、频次与注意事项优先于“卖点”。</li>
            <li>先讲选择：同类对比维度一致，减少“看不懂的差异”。</li>
          </ul>

          <h3>把“场景”放在第一位</h3>
          <p>
            农业不是在真空里发生的。我们更关注你当前的场景：是苗期还是花果期？是棚内还是露地？是高温干旱还是连阴雨？
            很多时候，答案不是“买更贵的”，而是“用更合适的”。
          </p>
          <p>
            所以我们希望平台的内容与结构，能把你从“猜”带到“判断”：先定位场景，再定位品类，再做具体选择。
          </p>

          <h3>我们相信：四季都有各自的节奏</h3>
          <p>
            春天是播种与起势，夏天是生长与管理，秋天是收获与总结，冬天是整理与准备。不同季节的关注点不同，
            平台也应该跟着节奏走：该强调什么、该提醒什么、该如何规划库存与采购，都应该更贴合真实种植周期。
          </p>

          <h3>我们的承诺</h3>
          <ul>
            <li>信息更清晰：让你少踩坑、少返工。</li>
            <li>选择更透明：让你能对比、能判断。</li>
            <li>服务更贴近：让建议更接近田间真实场景。</li>
          </ul>

          <h3>最后</h3>
          <p>
            如果你也喜欢星露谷，那你一定懂得：真正的提升不是“更快”，而是“更稳”。我们希望禾信综合农资平台能成为你
            长期使用的工具——像一把趁手的锄头、一套可靠的灌溉系统，安静但有用，陪你把每一季都过得更从容。
          </p>

          <p class="disclaimer">
            说明：本页面为“星露谷氛围”视觉致敬与体验设计，不与任何游戏/品牌存在官方关联。
          </p>
        </div>

        <footer class="article-foot">
          <button class="btn primary" type="button" @click="goProducts">进入商品中心</button>
          <button class="btn" type="button" @click="goHome">返回首页</button>
        </footer>
      </article>
    </main>
  </div>
</template>

<script>
export default {
  name: 'BrandStoryView',
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    heroImage() {
      // 使用 public/img 下现有图片，避免额外资源依赖
      return this.globalLightMode ? '/img/013.jpeg' : '/img/001.jpeg'
    },
    publishedAtISO() {
      return '2026-04-09'
    },
    publishedAtText() {
      return '2026 / 04 / 09'
    }
  },
  methods: {
    goProducts() {
      this.$router.push('/products')
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.story-page {
  --panel: rgba(23, 28, 40, 0.9);
  --line: #3f2f1f;
  --text: #f7e5be;
  --muted: #c2b295;
  --accent: #ffd46a;
  --accent2: #8ee6a2;
  min-height: 100vh;
  color: var(--text);
  font-family: 'Courier New', 'Lucida Console', monospace;
  background:
    linear-gradient(rgba(9, 11, 18, 0.55), rgba(9, 11, 18, 0.55)),
    radial-gradient(circle at 20% 10%, rgba(255, 212, 106, 0.18), transparent 42%),
    radial-gradient(circle at 80% 15%, rgba(142, 230, 162, 0.12), transparent 40%),
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: auto, auto, auto, 8px 8px, 8px 8px;
}

.story-main {
  width: min(1180px, 94%);
  margin: 0 auto;
  padding: 22px 0 60px;
}

.story-hero {
  min-height: clamp(520px, 66vh, 640px);
  border: 2px solid var(--line);
  background: var(--panel);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 8px 0 rgba(8, 10, 15, 0.42);
  overflow: hidden;
  position: relative;
}

.story-hero::after {
  content: '';
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: 0;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 212, 106, 0.75), rgba(255, 212, 106, 0.12));
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transform: scale(1.03);
  filter: saturate(1.05) contrast(1.05);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(10, 12, 18, 0.82), rgba(10, 12, 18, 0.28) 55%, rgba(10, 12, 18, 0.75)),
    radial-gradient(circle at 20% 20%, rgba(255, 212, 106, 0.18), transparent 45%),
    radial-gradient(circle at 80% 18%, rgba(142, 230, 162, 0.12), transparent 45%);
}

.hero-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 10px 10px;
  opacity: 0.45;
  pointer-events: none;
  mix-blend-mode: overlay;
}

.hero-content {
  position: relative;
  z-index: 1;
  height: 100%;
  padding: 22px;
  display: flex;
  align-items: flex-end;
}

.hero-left {
  width: min(760px, 100%);
  border: 2px solid rgba(101, 70, 42, 0.95);
  background: rgba(23, 28, 40, 0.82);
  box-shadow: 0 8px 0 rgba(0, 0, 0, 0.35);
  padding: 18px 18px 16px;
  backdrop-filter: blur(6px);
}

.kicker {
  color: var(--accent);
  font-size: 12px;
  letter-spacing: 1.6px;
}

.title {
  margin-top: 10px;
  font-size: clamp(28px, 3.2vw, 36px);
  letter-spacing: 0.6px;
}

.subtitle {
  margin-top: 12px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.75;
  max-width: 760px;
}

.chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  border: 2px solid #65462a;
  background: rgba(47, 56, 74, 0.7);
  color: #ffe5a8;
  padding: 6px 10px;
  font-size: 12px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 3px 0 rgba(0, 0, 0, 0.25);
}

.btn {
  height: 36px;
  border: 2px solid #65462a;
  background: #2f384a;
  color: #ffe5a8;
  cursor: pointer;
  padding: 0 14px;
  transition: transform 0.15s ease, filter 0.2s ease;
}

.btn:hover {
  filter: brightness(1.08);
}

.btn:active {
  transform: translateY(1px);
}

.btn.primary {
  background: linear-gradient(180deg, #ffd46a 0%, #d59f3d 100%);
  color: #1f160e;
  border-color: #9f6f3b;
}

.story-article {
  margin-top: 18px;
  border: 2px solid var(--line);
  background: var(--panel);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 8px 0 rgba(8, 10, 15, 0.42);
  padding: 18px;
}

.article-head {
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.2px;
}

.meta-pill {
  border: 2px solid #65462a;
  background: rgba(47, 56, 74, 0.65);
  color: #ffe5a8;
  padding: 3px 8px;
}

.meta-dot {
  opacity: 0.7;
}

.article-title {
  margin-top: 10px;
  font-size: 22px;
  letter-spacing: 0.4px;
}

.article-lead {
  margin-top: 10px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.75;
  max-width: 860px;
}

.prose {
  padding-top: 14px;
  font-size: 14px;
  line-height: 1.9;
  color: var(--text);
}

.prose h3 {
  margin-top: 18px;
  font-size: 16px;
  letter-spacing: 0.2px;
  color: #ffe5a8;
}

.prose p {
  margin-top: 10px;
  color: var(--muted);
}

.prose ul {
  margin-top: 10px;
  padding-left: 18px;
  list-style: square;
  color: var(--muted);
}

.prose li {
  margin-top: 6px;
}

.prose blockquote {
  margin-top: 12px;
  border-left: 4px solid rgba(255, 212, 106, 0.7);
  background: rgba(37, 44, 58, 0.55);
  padding: 12px 12px 12px 14px;
  color: #e7d6b5;
}

.disclaimer {
  margin-top: 16px;
  font-size: 12px;
  color: #a89a86;
}

.article-foot {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.story-page.light-mode {
  --panel: rgba(250, 242, 230, 0.92);
  --line: #9a7348;
  --text: #3f2c1f;
  --muted: #5d4f43;
  --accent: #9d621f;
  --accent2: #2f7a4a;
  background:
    linear-gradient(rgba(255, 248, 236, 0), rgba(255, 248, 236, 0)),
    radial-gradient(circle at 20% 10%, rgba(157, 98, 31, 0.12), transparent 44%),
    radial-gradient(circle at 80% 15%, rgba(47, 122, 74, 0.1), transparent 42%),
    linear-gradient(rgba(66, 49, 32, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(66, 49, 32, 0.07) 1px, transparent 1px);
  background-size: auto, auto, auto, 8px 8px, 8px 8px;
}

.story-page.light-mode .chip,
.story-page.light-mode .btn,
.story-page.light-mode .meta-pill {
  background: #f8f0e2;
  color: #3f2c1f;
  border-color: #9a7348;
  box-shadow: 0 4px 0 rgba(138, 100, 64, 0.16);
}

.story-page.light-mode .btn.primary {
  background: linear-gradient(180deg, #d7c0a0 0%, #b7956f 100%);
  color: #2b1b10;
}

.story-page.light-mode .hero-left {
  border-color: rgba(154, 115, 72, 0.95);
  background: rgba(248, 240, 226, 0.84);
  box-shadow: 0 8px 0 rgba(138, 100, 64, 0.18);
}

.story-page.light-mode .prose h3 {
  color: #5f3c1e;
}

.story-page.light-mode .prose blockquote {
  border-left-color: rgba(157, 98, 31, 0.6);
  background: rgba(236, 225, 208, 0.7);
  color: #5f3c1e;
}

@media (max-width: 980px) {
  .hero-content {
    display: block;
    align-items: start;
  }
}

@media (max-width: 540px) {
  .story-main {
    width: 94%;
  }

  .hero-content {
    padding: 14px;
  }

  .story-article {
    padding: 14px;
  }
}
</style>
