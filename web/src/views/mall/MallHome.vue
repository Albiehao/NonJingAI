<template>
  <div class="mall-home">
    <div class="mall-header">
      <h1 class="mall-title">商城</h1>
      <p class="mall-subtitle">浏览农资商品，分类筛选与关键词搜索</p>
    </div>

    <div class="toolbar">
      <a-input-search
          v-model:value="keyword"
          placeholder="搜索商品名称 / 品牌"
          allow-clear
          class="search-input"
          @search="handleSearch"
          @pressEnter="handleSearch"
      />
    </div>

    <a-tabs v-model:activeKey="activeCategory" class="category-tabs" @change="handleCategoryChange">
      <a-tab-pane key="all" tab="全部" />
      <a-tab-pane v-for="cat in categories" :key="String(cat.id)" :tab="cat.name" />
    </a-tabs>

    <a-spin :spinning="loading" tip="加载中...">
      <div v-if="products.length" class="product-grid">
        <div v-for="item in products" :key="item.id" class="product-card" @click="goDetail(item.id)">
          <div class="card-img-wrap">
            <img :src="item.mainImage || '/img/001.jpeg'" :alt="item.productName" class="card-img" />
          </div>
          <div class="card-body">
            <h3 class="card-name">{{ item.productName }}</h3>
            <span class="card-brand">{{ item.brand }}</span>
            <div class="card-price">¥{{ formatPrice(item.price) }}</div>
            <div class="card-actions">
              <a-button size="small" @click.stop="handleAddCart(item)">
                <template #icon><ShoppingCartIcon :size="14" /></template>
                加入购物车
              </a-button>
              <a-button type="primary" size="small" @click.stop="handleBuyNow(item)">
                立即购买
              </a-button>
            </div>
          </div>
        </div>
      </div>

      <a-empty v-else-if="!loading" description="暂无商品数据" class="empty-state" />
    </a-spin>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { ShoppingCart as ShoppingCartIcon } from 'lucide-vue-next'
import {
  getCategories,
  getAllProducts,
  getProductsByCategoryId,
  searchProducts
} from '@/apis/mall'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()



const categories = ref([])
const products = ref([])
const loading = ref(false)
const keyword = ref('')
const activeCategory = ref('all')

const formatPrice = (price) => Number(price || 0).toFixed(2)

const loadCategories = async () => {
  try {
    const res = await getCategories()
    if (res.code === 0) categories.value = res.data || []
  } catch (e) {
    console.error('加载分类失败', e)
  }
}

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await getAllProducts()
    if (res.code === 0) products.value = res.data || []
  } catch (e) {
    console.error('加载商品失败', e)
    message.error('加载商品失败')
  } finally {
    loading.value = false
  }
}

const handleCategoryChange = async (key) => {
  keyword.value = ''
  loading.value = true
  try {
    if (key === 'all') {
      const res = await getAllProducts()
      if (res.code === 0) products.value = res.data || []
    } else {
      const res = await getProductsByCategoryId(key)
      if (res.code === 0) products.value = res.data || []
    }
  } catch (e) {
    message.error('加载商品失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = async () => {
  activeCategory.value = 'all'
  loading.value = true
  try {
    if (!keyword.value.trim()) {
      const res = await getAllProducts()
      if (res.code === 0) products.value = res.data || []
    } else {
      const res = await searchProducts(keyword.value.trim())
      if (res.code === 0) products.value = res.data || []
    }
  } catch (e) {
    message.error('搜索失败')
  } finally {
    loading.value = false
  }
}

const handleAddCart = (item) => {
  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }
  cartStore.addToCart(item.id, 1, {
    productName: item.productName,
    mainImage: item.mainImage,
    price: item.price
  })
  message.success('已加入购物车')
}


const handleBuyNow = (item) => {
  router.push(`/mall/${item.id}`)
}

const goDetail = (id) => {
  router.push(`/mall/${id}`)
}

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<style lang="less" scoped>
.mall-home {
  padding: 24px;
  min-height: 100%;
}

.mall-header {
  margin-bottom: 20px;
}

.mall-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 6px;
}

.mall-subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

.toolbar {
  margin-bottom: 16px;
  max-width: 400px;
}

.category-tabs {
  margin-bottom: 8px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  border: 1px solid var(--gray-100);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.15s;

  &:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }
}

.card-img-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background: var(--gray-50, #f9fafb);
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.card-body {
  padding: 12px;
}

.card-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-brand {
  font-size: 12px;
  color: var(--gray-500);
}

.card-price {
  font-size: 18px;
  font-weight: 700;
  color: #e85d2f;
  margin: 8px 0;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 60px 0;
}

@media (max-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
