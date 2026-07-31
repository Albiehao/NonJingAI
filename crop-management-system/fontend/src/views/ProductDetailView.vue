<template>
  <div class="product-detail-page" :class="{ 'light-mode': globalLightMode }">
    <main class="detail-main">
      <section v-if="product" class="detail-shell">
        <div class="detail-topbar">
          <button class="back-btn" type="button" @click="goBack">
            <span class="back-icon">&#8592;</span>
            返回商品页
          </button>
          <div class="detail-breadcrumb">
            <span>商品详情</span>
            <span>/</span>
            <span>{{ categoryName || '未分类' }}</span>
          </div>
        </div>

        <section class="detail-hero">
          <div class="media-panel">
            <div class="media-stage">
              <img class="detail-image" :src="product.mainImage || '/img/001.jpeg'" :alt="product.productName" />
            </div>
          </div>

          <div class="info-panel">
            <p class="info-kicker">HEXIN AGRI PRODUCT</p>
            <h1 class="info-title">{{ product.productName }}</h1>
            <p class="info-desc">{{ product.description || '暂无商品描述' }}</p>

            <div class="price-panel">
              <div>
                <span class="price-label">参考价格</span>
                <div class="price-row">
                  <span class="price-symbol">¥</span>
                  <span class="price-value">{{ formatPrice(product.price) }}</span>
                </div>
              </div>
              <button class="buy-channel-btn" type="button" @click="openChannels">购买渠道</button>
            </div>

            <div class="detail-summary">
              <div class="summary-row">
                <span class="summary-label">品牌</span>
                <span class="summary-value">{{ product.brand || '禾信优选' }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">编号</span>
                <span class="summary-value">{{ product.productCode || product.id }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">规格</span>
                <span class="summary-value">{{ product.contentSpec || '暂无' }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">剂型</span>
                <span class="summary-value">{{ product.formulation || '暂无' }}</span>
              </div>
              <div class="summary-row full">
                <span class="summary-label">适用作物</span>
                <span class="summary-value">{{ product.useCrops || '暂无' }}</span>
              </div>
              <div class="summary-row full">
                <span class="summary-label">使用方法</span>
                <span class="summary-value">{{ product.usageMethod || '暂无' }}</span>
              </div>
              <div class="summary-row full">
                <span class="summary-label">注意事项</span>
                <span class="summary-value">{{ product.precautions || '暂无' }}</span>
              </div>
            </div>
          </div>
        </section>
      </section>

      <section v-else class="empty-panel">
        <div class="empty-icon">&#128269;</div>
        <p class="empty-title">未找到该商品</p>
        <p class="empty-desc">可能已下架，或当前编号不存在。</p>
        <button class="back-btn" type="button" @click="goBack">
          <span class="back-icon">&#8592;</span>
          返回商品页
        </button>
      </section>

      <div v-if="channelVisible" class="channel-mask" @click="closeChannels">
        <section class="channel-modal" role="dialog" aria-modal="true" @click.stop>
          <div class="channel-head">
            <div>
              <p class="card-kicker">BUY CHANNELS</p>
              <h3 class="channel-title">购买渠道</h3>
            </div>
            <button type="button" class="channel-close" @click="closeChannels">关闭</button>
          </div>
          <p class="channel-tip">以下为常用购买渠道，可根据价格、时效和店铺信誉选择。</p>
          <div class="channel-grid">
            <a
              v-for="item in purchaseChannels"
              :key="item.name"
              class="channel-item"
              :href="item.url"
              target="_blank"
              rel="noopener"
            >
              <span class="channel-name">{{ item.name }}</span>
              <span class="channel-desc">{{ item.desc }}</span>
              <span class="channel-arrow">&#8594;</span>
            </a>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import { getAgrochemicalById } from '@/api/agrochemicals'
import { getCategoryById } from '@/api/categories'

export default {
  name: 'ProductDetailView',
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      product: null,
      categoryName: '',
      channelVisible: false,
      purchaseChannels: [
        { name: '京东', url: 'https://www.jd.com/', desc: '适合查看自营与品牌店铺' },
        { name: '拼多多', url: 'https://www.pinduoduo.com/', desc: '适合比价与活动采购' },
        { name: '淘宝', url: 'https://www.taobao.com/', desc: '店铺多，商品覆盖更广' },
        { name: '品牌商城', url: 'https://example.com/', desc: '适合查看官方渠道信息' }
      ]
    }
  },
  created() {
    this.loadProduct()
  },
  watch: {
    '$route.params.id': 'loadProduct'
  },
  methods: {
    async loadProduct() {
      const id = this.$route.params.id
      try {
        const res = await getAgrochemicalById(id)
        if (res.code === 0 && res.data) {
          this.product = res.data
          this.categoryName = ''
          if (this.product.categoryId) {
            const catRes = await getCategoryById(this.product.categoryId)
            if (catRes.code === 0 && catRes.data) {
              this.categoryName = catRes.data.name
            }
          }
        } else {
          this.product = null
        }
      } catch (e) {
        this.product = null
      }
    },
    formatPrice(price) {
      return Number(price || 0).toFixed(2)
    },
    openChannels() {
      this.channelVisible = true
    },
    closeChannels() {
      this.channelVisible = false
    },
    goBack() {
      this.$router.push('/products')
    }
  }
}
</script>

<style scoped>
.product-detail-page {
  --panel: rgba(23, 28, 40, 0.92);
  --panel-strong: rgba(18, 22, 31, 0.96);
  --card: #252c3a;
  --line: #4b351f;
  --line-strong: #7d5832;
  --text: #f7e5be;
  --muted: #c2b295;
  --accent: #ffd46a;
  min-height: 100vh;
  background:
    linear-gradient(rgba(9, 11, 18, 0.6), rgba(9, 11, 18, 0.6)),
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  color: var(--text);
  font-family: 'Courier New', 'Lucida Console', monospace;
}

.product-detail-page.light-mode {
  --panel: rgba(250, 242, 230, 0.93);
  --panel-strong: rgba(244, 234, 220, 0.97);
  --card: #f8f0e2;
  --line: #9a7348;
  --line-strong: #6f4c30;
  --text: #3f2c1f;
  --muted: #5d4f43;
  --accent: #9d621f;
  background:
    linear-gradient(rgba(255, 248, 236, 0.08), rgba(255, 248, 236, 0.08)),
    linear-gradient(rgba(66, 49, 32, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(66, 49, 32, 0.06) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
}

.detail-main {
  width: min(980px, 94%);
  margin: 0 auto;
  padding: 20px 0 44px;
}

.detail-shell {
  display: grid;
  gap: 14px;
}

.detail-topbar,
.detail-hero,
.empty-panel,
.channel-modal {
  border: 2px solid var(--line);
  background: var(--panel);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 6px 0 rgba(8, 10, 15, 0.32);
}

.detail-topbar {
  padding: 12px 14px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.back-btn,
.buy-channel-btn,
.channel-close {
  height: 38px;
  border: 2px solid var(--line);
  background: var(--card);
  color: var(--text);
  padding: 0 14px;
  font-family: inherit;
  font-size: 12px;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), inset 0 -2px 0 rgba(0, 0, 0, 0.24);
}

.back-btn:hover,
.buy-channel-btn:hover,
.channel-close:hover,
.channel-item:hover {
  filter: brightness(1.06);
}

.back-btn:active,
.buy-channel-btn:active,
.channel-close:active {
  transform: translateY(1px);
}

.back-icon {
  margin-right: 6px;
}

.detail-breadcrumb {
  display: inline-flex;
  gap: 8px;
  color: var(--muted);
  font-size: 11px;
}

.detail-hero {
  padding: 16px;
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 16px;
}

.media-panel,
.info-panel {
  min-width: 0;
}

.media-stage {
  padding: 8px;
  border: 2px solid var(--line);
  background: var(--panel-strong);
}

.detail-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  display: block;
  border: 2px solid var(--line);
}

.info-kicker,
.card-kicker {
  color: var(--accent);
  font-size: 11px;
  letter-spacing: 1.6px;
}

.info-title {
  margin-top: 8px;
  font-size: clamp(24px, 2.4vw, 30px);
  line-height: 1.25;
}

.info-desc {
  margin-top: 10px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
}

.price-panel {
  margin-top: 14px;
  padding: 14px;
  border: 2px solid var(--line);
  background: var(--panel-strong);
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 14px;
  flex-wrap: wrap;
}

.price-label {
  display: block;
  color: var(--muted);
  font-size: 11px;
}

.price-row {
  margin-top: 4px;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-symbol {
  color: var(--accent);
  font-size: 16px;
}

.price-value {
  color: var(--accent);
  font-size: 28px;
  font-weight: 700;
}

.detail-summary {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.summary-row {
  padding: 10px 12px;
  border: 2px solid var(--line);
  background: var(--card);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.summary-row.full {
  grid-column: 1 / -1;
}

.summary-label {
  color: var(--muted);
  font-size: 11px;
}

.summary-value {
  font-size: 13px;
  line-height: 1.7;
}

.empty-panel {
  padding: 32px 22px;
  text-align: center;
}

.empty-icon {
  font-size: 42px;
  color: var(--accent);
}

.empty-title {
  margin-top: 14px;
  font-size: 20px;
}

.empty-desc {
  margin-top: 10px;
  color: var(--muted);
  font-size: 13px;
}

.empty-panel .back-btn {
  margin-top: 18px;
}

.channel-mask {
  position: fixed;
  inset: 0;
  z-index: 80;
  background: rgba(12, 14, 22, 0.72);
  display: flex;
  align-items: center;
  justify-content: center;
}

.channel-modal {
  width: min(500px, calc(100vw - 24px));
  padding: 16px;
}

.channel-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: start;
}

.channel-title {
  margin-top: 6px;
  font-size: 20px;
}

.channel-tip {
  margin-top: 12px;
  color: var(--muted);
  font-size: 12px;
}

.channel-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.channel-item {
  padding: 14px;
  border: 2px solid var(--line);
  background: var(--card);
  color: var(--text);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}

.channel-name {
  font-size: 14px;
}

.channel-desc {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
}

.channel-arrow {
  position: absolute;
  right: 12px;
  top: 14px;
  color: var(--accent);
}

@media (max-width: 980px) {
  .detail-hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .detail-main {
    width: min(100%, 94%);
  }

  .detail-summary,
  .channel-grid {
    grid-template-columns: 1fr;
  }

  .price-panel,
  .detail-topbar {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
