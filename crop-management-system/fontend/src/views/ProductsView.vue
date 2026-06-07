<template>
  <div class="products-page" :class="{ 'light-mode': globalLightMode }">
    <main class="products-main">
      <section class="products-hero">
        <p class="hero-kicker">AGRI E-COMMERCE</p>
        <h1 class="hero-title">商品中心</h1>
        <p class="hero-desc">支持关键词搜索、分类筛选、价格筛选与分页浏览，快速找到目标商品。</p>
      </section>

      <section class="products-panel">
        <div class="filter-bar">
          <input
            v-model.trim="searchKeyword"
            class="filter-input"
            type="text"
            placeholder="搜索商品名称 / 品牌 / 说明"
          />
          <div class="filter-select-wrap" @click.stop>
            <button type="button" class="filter-select-trigger" @click="toggleDropdown('parent')">
              {{ selectedParentCategory || '一级分类' }}
            </button>
            <ul v-if="parentOpen" class="filter-select-menu">
              <li :class="{ active: selectedParentCategory === '' }" @click="setParentCategory('')">全部一级</li>
              <li
                v-for="item in parentCategories"
                :key="item.id"
                :class="{ active: selectedParentCategory === item.name }"
                @click="setParentCategory(item)"
              >
                {{ item.name }}
              </li>
            </ul>
          </div>
          <div class="filter-select-wrap" @click.stop>
            <button
              type="button"
              class="filter-select-trigger"
              :disabled="!selectedParentCategory"
              @click="toggleDropdown('child')"
            >
              {{ selectedChildCategory || '二级分类' }}
            </button>
            <ul v-if="childOpen" class="filter-select-menu">
              <li :class="{ active: selectedChildCategory === '' }" @click="setChildCategory('')">全部二级</li>
              <li
                v-for="item in childCategories"
                :key="item.id"
                :class="{ active: selectedChildCategory === item.name }"
                @click="setChildCategory(item)"
              >
                {{ item.name }}
              </li>
            </ul>
          </div>
          <div class="filter-select-wrap" @click.stop>
            <button type="button" class="filter-select-trigger" @click="toggleDropdown('price')">
              {{ selectedPriceLabel }}
            </button>
            <ul v-if="priceOpen" class="filter-select-menu">
              <li :class="{ active: selectedPriceRange === '' }" @click="setPriceRange('')">全部价格</li>
              <li :class="{ active: selectedPriceRange === '0-99' }" @click="setPriceRange('0-99')">100 元以下</li>
              <li :class="{ active: selectedPriceRange === '100-199' }" @click="setPriceRange('100-199')">100 - 199 元</li>
              <li :class="{ active: selectedPriceRange === '200-399' }" @click="setPriceRange('200-399')">200 - 399 元</li>
              <li :class="{ active: selectedPriceRange === '400+' }" @click="setPriceRange('400+')">400 元及以上</li>
            </ul>
          </div>
          <button class="filter-reset" type="button" @click="resetFilters">重置筛选</button>
        </div>

        <div class="result-tip">
          共 <strong>{{ filteredProducts.length }}</strong> 件商品，当前第 <strong>{{ currentPage }}</strong> /
          <strong>{{ totalPages }}</strong> 页
        </div>

        <div v-if="pagedProducts.length" class="product-grid">
          <article v-for="item in pagedProducts" :key="item.id" class="product-card">
            <img class="product-image" :src="item.mainImage || '/img/001.jpeg'" :alt="item.productName" />
            <p class="product-category">{{ getCategoryName(item.categoryId) }}</p>
            <h3 class="product-name">{{ item.productName }}</h3>
            <p class="product-desc">{{ item.description || item.contentSpec || '暂无描述' }}</p>
            <div class="product-meta">
              <span class="product-brand">{{ item.brand || '禾信优选' }}</span>
              <span class="product-sales">月销 {{ item.monthlySales || 0 }}</span>
            </div>
            <div class="product-bottom">
              <p class="product-price">¥{{ formatPrice(item.price) }}</p>
              <button class="product-buy" type="button" @click="goDetail(item)">查看详情</button>
            </div>
          </article>
        </div>
        <div v-else class="empty-state">没有符合条件的商品，请调整筛选条件。</div>

        <div class="pagination-row">
          <div v-if="totalPages > 1" class="pagination">
            <button type="button" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">上一页</button>
            <button
              v-for="page in totalPages"
              :key="page"
              type="button"
              :class="{ active: page === currentPage }"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
            <button type="button" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              下一页
            </button>
          </div>
          <div class="page-size-control">
            <label for="page-size-select">每页显示</label>
            <select id="page-size-select" v-model.number="pageSize">
              <option :value="8">8</option>
              <option :value="12">12</option>
              <option :value="16">16</option>
              <option :value="24">24</option>
            </select>
            <span>件</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { getAllAgrochemicals } from '@/api/agrochemicals'
import { getAllCategories } from '@/api/categories'

export default {
  name: 'ProductsView',
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      products: [],
      categories: [],
      searchKeyword: '',
      selectedParentCategory: '',
      selectedChildCategory: '',
      selectedPriceRange: '',
      parentOpen: false,
      childOpen: false,
      priceOpen: false,
      currentPage: 1,
      pageSize: 8
    }
  },
  computed: {
    parentCategories() {
      return this.categories.filter(c => !c.parentId)
    },
    childCategories() {
      if (!this.selectedParentCategory) return []
      const parentId = this.parentCategories.find(p => p.name === this.selectedParentCategory)?.id
      return this.categories.filter(c => c.parentId === parentId)
    },
    selectedPriceLabel() {
      if (this.selectedPriceRange === '0-99') return '100 元以下'
      if (this.selectedPriceRange === '100-199') return '100 - 199 元'
      if (this.selectedPriceRange === '200-399') return '200 - 399 元'
      if (this.selectedPriceRange === '400+') return '400 元及以上'
      return '全部价格'
    },
    filteredProducts() {
      return this.products.filter((item) => {
        const keyword = this.searchKeyword.toLowerCase()
        const keywordMatched =
          !keyword ||
          [item.productName, item.brand, item.description]
            .join(' ')
            .toLowerCase()
            .includes(keyword)

        const categoryMatched = !this.selectedChildCategory ||
          this.getCategoryName(item.categoryId) === this.selectedChildCategory

        const priceMatched = this.matchPrice(item.price)
        return keywordMatched && categoryMatched && priceMatched
      })
    },
    totalPages() {
      const pages = Math.ceil(this.filteredProducts.length / this.pageSize)
      return pages > 0 ? pages : 1
    },
    pagedProducts() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredProducts.slice(start, start + this.pageSize)
    }
  },
  watch: {
    searchKeyword() {
      this.currentPage = 1
    },
    selectedParentCategory() {
      this.currentPage = 1
      this.selectedChildCategory = ''
    },
    selectedChildCategory() {
      this.currentPage = 1
    },
    selectedPriceRange() {
      this.currentPage = 1
    },
    pageSize() {
      this.currentPage = 1
    },
    filteredProducts() {
      if (this.currentPage > this.totalPages) {
        this.currentPage = this.totalPages
      }
    }
  },
  created() {
    this.loadData()
  },
  mounted() {
    document.addEventListener('click', this.closeDropdowns)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeDropdowns)
  },
  methods: {
    async loadData() {
      try {
        const [catRes, prodRes] = await Promise.all([
          getAllCategories(),
          getAllAgrochemicals()
        ])
        if (catRes.code === 0) this.categories = catRes.data || []
        if (prodRes.code === 0) this.products = prodRes.data || []
      } catch (e) {
        console.error('加载数据失败', e)
      }
    },
    getCategoryName(categoryId) {
      const cat = this.categories.find(c => c.id === categoryId)
      return cat?.name || '未分类'
    },
    matchPrice(price) {
      if (!this.selectedPriceRange) return true
      const p = Number(price) || 0
      if (this.selectedPriceRange === '0-99') return p <= 99
      if (this.selectedPriceRange === '100-199') return p >= 100 && p <= 199
      if (this.selectedPriceRange === '200-399') return p >= 200 && p <= 399
      if (this.selectedPriceRange === '400+') return p >= 400
      return true
    },
    resetFilters() {
      this.searchKeyword = ''
      this.selectedParentCategory = ''
      this.selectedChildCategory = ''
      this.selectedPriceRange = ''
      this.closeDropdowns()
      this.currentPage = 1
    },
    toggleDropdown(type) {
      if (type === 'parent') {
        this.parentOpen = !this.parentOpen
        this.childOpen = false
        this.priceOpen = false
        return
      }
      if (type === 'child') {
        if (!this.selectedParentCategory) return
        this.childOpen = !this.childOpen
        this.parentOpen = false
        this.priceOpen = false
        return
      }
      this.priceOpen = !this.priceOpen
      this.parentOpen = false
      this.childOpen = false
    },
    closeDropdowns() {
      this.parentOpen = false
      this.childOpen = false
      this.priceOpen = false
    },
    setParentCategory(item) {
      this.selectedParentCategory = item?.name || ''
      this.selectedChildCategory = ''
      this.parentOpen = false
    },
    setChildCategory(item) {
      this.selectedChildCategory = item?.name || ''
      this.childOpen = false
    },
    setPriceRange(value) {
      this.selectedPriceRange = value
      this.closeDropdowns()
    },
    goToPage(page) {
      if (page < 1 || page > this.totalPages) return
      this.currentPage = page
    },
    formatPrice(price) {
      return Number(price || 0).toFixed(2)
    },
    goDetail(item) {
      this.$router.push(`/products/${item.id}`)
    }
  }
}
</script>

<style scoped>
.products-page {
  --panel: rgba(23, 28, 40, 0.9);
  --line: #3f2f1f;
  --text: #f7e5be;
  --muted: #c2b295;
  --accent: #ffd46a;
  min-height: 100vh;
  background:
    linear-gradient(rgba(9, 11, 18, 0.58), rgba(9, 11, 18, 0.58)),
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  color: var(--text);
  font-family: 'Courier New', 'Lucida Console', monospace;
}

.products-main {
  width: min(1180px, 94%);
  margin: 0 auto;
  padding: 26px 0 56px;
}

.products-hero,
.products-panel {
  border: 2px solid var(--line);
  background: var(--panel);
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 8px 0 rgba(8, 10, 15, 0.42);
}

.products-hero {
  position: relative;
  padding: 22px 24px 20px;
  overflow: hidden;
}

.products-hero::after {
  content: '';
  position: absolute;
  left: 24px;
  right: 24px;
  bottom: 0;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 212, 106, 0.75), rgba(255, 212, 106, 0.12));
}

.hero-kicker {
  color: var(--accent);
  font-size: 12px;
  letter-spacing: 1.5px;
}

.hero-title {
  margin-top: 10px;
  font-size: clamp(28px, 3.2vw, 34px);
  letter-spacing: 0.8px;
}

.hero-desc {
  margin-top: 12px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
  max-width: 760px;
}

.products-panel {
  margin-top: 18px;
  padding: 18px 18px 20px;
}

.filter-bar {
  display: grid;
  grid-template-columns: minmax(220px, 2.2fr) minmax(140px, 1fr) minmax(140px, 1fr) minmax(140px, 1fr) auto;
  gap: 10px;
  align-items: center;
}

.filter-input,
.filter-select-trigger {
  height: 34px;
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f7e5be;
  padding: 0 10px;
  font-family: inherit;
  font-size: 12px;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.filter-input::placeholder {
  color: #8e98a8;
}

.filter-input:focus,
.filter-select-trigger:focus {
  outline: none;
  border-color: #8d6b4b;
  background: #333a45;
  box-shadow:
    0 0 0 2px rgba(141, 107, 75, 0.36),
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.filter-select-wrap {
  position: relative;
}

.filter-select-trigger {
  width: 100%;
  text-align: left;
  cursor: pointer;
  position: relative;
  padding-right: 32px;
  font-family: inherit;
}

.filter-select-trigger::after {
  content: '';
  position: absolute;
  right: 10px;
  top: 50%;
  width: 9px;
  height: 9px;
  transform: translateY(-60%) rotate(45deg);
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
}

.filter-select-menu {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  border: 2px solid #65462a;
  background: #2b3038;
  box-shadow: 0 6px 0 #1a2230;
  z-index: 15;
  max-height: 240px;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.filter-select-menu::-webkit-scrollbar {
  width: 0;
  height: 0;
  display: none;
}

.filter-select-menu li {
  padding: 10px 12px;
  color: #f7e5be;
  cursor: pointer;
}

.filter-select-menu li:hover,
.filter-select-menu li.active {
  background: #333a45;
  color: #ffe5a8;
}

.filter-reset {
  height: 34px;
  border: 2px solid #65462a;
  background: #2f384a;
  color: #ffe5a8;
  cursor: pointer;
  padding: 0 12px;
  font-size: 12px;
  transition: transform 0.15s ease, box-shadow 0.2s ease, filter 0.2s ease;
}

.filter-reset:hover {
  filter: brightness(1.08);
}

.filter-reset:active {
  transform: translateY(1px);
}

.result-tip {
  margin-top: 14px;
  color: var(--muted);
  font-size: 13px;
}

.product-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.product-card {
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 4px 0 #1a2230;
  padding: 10px;
  transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.product-card:hover {
  transform: translateY(-2px);
  border-color: #9f6f3b;
  box-shadow: 0 6px 0 #1a2230;
}

.product-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  display: block;
  border: 2px solid #3d2b1b;
}

.product-category {
  margin-top: 8px;
  font-size: 11px;
  color: #d5ae63;
}

.product-name {
  margin-top: 6px;
  font-size: 15px;
  color: #ffe5a8;
}

.product-desc {
  margin-top: 8px;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
  min-height: 38px;
}

.product-meta {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #cbbca2;
}

.product-bottom {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  color: #ffd46a;
  font-size: 18px;
  font-weight: 700;
}

.product-buy {
  border: 2px solid #65462a;
  background: #2f384a;
  color: #ffe5a8;
  height: 34px;
  padding: 0 12px;
  cursor: pointer;
  transition: transform 0.15s ease, filter 0.2s ease;
}

.product-buy:hover {
  filter: brightness(1.08);
}

.product-buy:active {
  transform: translateY(1px);
}

.empty-state {
  margin-top: 18px;
  border: 2px dashed #65462a;
  color: #d5ae63;
  padding: 22px;
  text-align: center;
  background: rgba(37, 44, 58, 0.5);
}

.pagination {
  margin-top: 18px;
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.pagination button {
  min-width: 36px;
  height: 34px;
  border: 2px solid #65462a;
  background: #2f384a;
  color: #ffe5a8;
  cursor: pointer;
  transition: transform 0.15s ease, filter 0.2s ease;
}

.pagination button:hover:not([disabled]) {
  filter: brightness(1.08);
}

.pagination button:active:not([disabled]) {
  transform: translateY(1px);
}

.pagination button.active {
  background: #ffd46a;
  color: #1f160e;
}

.pagination button[disabled] {
  opacity: 0.45;
  cursor: not-allowed;
}

.pagination-row {
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.page-size-control {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
}

.page-size-control select {
  width: 84px;
  height: 34px;
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f7e5be;
  padding: 0 8px;
  font-family: inherit;
  outline: none;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.page-size-control select:focus {
  border-color: #8d6b4b;
  background: #333a45;
  box-shadow:
    0 0 0 2px rgba(141, 107, 75, 0.36),
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.products-page.light-mode {
  --panel: rgba(250, 242, 230, 0.92);
  --line: #9a7348;
  --text: #3f2c1f;
  --muted: #5d4f43;
  --accent: #9d621f;
  background:
    linear-gradient(rgba(255, 248, 236, 0), rgba(255, 248, 236, 0)),
    linear-gradient(rgba(66, 49, 32, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(66, 49, 32, 0.07) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
}

.products-page.light-mode .filter-input,
.products-page.light-mode .filter-select-trigger,
.products-page.light-mode .filter-reset,
.products-page.light-mode .product-card,
.products-page.light-mode .product-buy,
.products-page.light-mode .pagination button,
.products-page.light-mode .page-size-control select {
  background: #f8f0e2;
  color: #3f2c1f;
  border-color: #9a7348;
}

.products-page.light-mode .filter-input::placeholder {
  color: #8a7a68;
}

.products-page.light-mode .filter-input:focus,
.products-page.light-mode .filter-select-trigger:focus {
  background: #ece1d0;
  border-color: #6f4c30;
  box-shadow:
    0 0 0 2px rgba(111, 76, 48, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.products-page.light-mode .filter-select-menu {
  background: #f1e9db;
  border-color: #8d6b4b;
  box-shadow: 0 6px 0 rgba(138, 100, 64, 0.16);
}

.products-page.light-mode .filter-select-menu li {
  color: #433224;
}

.products-page.light-mode .filter-select-menu li:hover,
.products-page.light-mode .filter-select-menu li.active {
  background: #ece1d0;
  color: #5f3c1e;
}

.products-page.light-mode .product-name {
  color: #5f3c1e;
}

.products-page.light-mode .product-price {
  color: #9d621f;
}

@media (max-width: 1000px) {
  .product-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 800px) {
  .filter-bar {
    grid-template-columns: 1fr;
  }

  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1100px) {
  .filter-bar {
    grid-template-columns: 1.6fr 1fr 1fr auto;
  }

  .filter-bar .filter-select-wrap:nth-of-type(2) {
    display: none;
  }
}

@media (max-width: 540px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
