<template>
  <div class="mall-detail">
    <a-spin :spinning="loading" tip="加载中...">
      <template v-if="product">
        <div class="detail-breadcrumb">
          <router-link to="/mall">商城</router-link>
          <span class="sep">/</span>
          <span class="current">{{ product.productName }}</span>
        </div>

        <div class="detail-main">
          <div class="detail-gallery">
            <img :src="product.mainImage || '/img/001.jpeg'" :alt="product.productName" class="detail-img" />
          </div>

          <div class="detail-info">
            <h1 class="detail-title">{{ product.productName }}</h1>
            <p class="detail-brand">{{ product.brand }}</p>

            <div class="detail-price-row">
              <span class="detail-price">¥{{ formatPrice(product.price) }}</span>
              <a-tag v-if="product.monthlySales" color="orange">月销 {{ product.monthlySales }}</a-tag>
            </div>

            <p v-if="product.description" class="detail-desc">{{ product.description }}</p>

            <a-descriptions :column="1" bordered size="small" class="detail-specs">
              <a-descriptions-item v-if="product.registrationNo" label="登记证号">
                {{ product.registrationNo }}
              </a-descriptions-item>
              <a-descriptions-item v-if="product.formulation" label="剂型">
                {{ product.formulation }}
              </a-descriptions-item>
              <a-descriptions-item v-if="product.contentSpec" label="规格">
                {{ product.contentSpec }}
              </a-descriptions-item>
              <a-descriptions-item v-if="product.useCrops" label="适用作物">
                {{ product.useCrops }}
              </a-descriptions-item>
              <a-descriptions-item v-if="product.usageMethod" label="使用方法">
                {{ product.usageMethod }}
              </a-descriptions-item>
              <a-descriptions-item v-if="product.precautions" label="注意事项">
                {{ product.precautions }}
              </a-descriptions-item>
            </a-descriptions>

            <div class="detail-actions">
              <div class="qty-row">
                <span class="qty-label">数量</span>
                <a-input-number v-model:value="quantity" :min="1" :max="99" />
              </div>
              <div class="btn-row">
                <a-button size="large" @click="handleAddCart" :loading="cartLoading">
                  <template #icon><ShoppingCartIcon :size="16" /></template>
                  加入购物车
                </a-button>
                <a-button type="primary" size="large" @click="handleBuyNow" :loading="buyLoading">
                  立即购买
                </a-button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <a-result v-else-if="!loading" status="404" title="商品不存在" sub-title="该商品可能已下架或编号有误">
        <template #extra>
          <router-link to="/mall">
            <a-button type="primary">返回商城</a-button>
          </router-link>
        </template>
      </a-result>
    </a-spin>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { ShoppingCart as ShoppingCartIcon } from 'lucide-vue-next'
import { getProductById } from '@/apis/mall'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()


const product = ref(null)
const loading = ref(false)
const cartLoading = ref(false)
const buyLoading = ref(false)
const quantity = ref(1)

const formatPrice = (price) => Number(price || 0).toFixed(2)

const loadProduct = async () => {
  const id = route.params.id
  loading.value = true
  product.value = null
  quantity.value = 1
  try {
    const res = await getProductById(id)
    if (res.code === 0 && res.data) {
      product.value = res.data
    }
  } catch (e) {
    console.error('加载商品详情失败', e)
    message.error('加载商品详情失败')
  } finally {
    loading.value = false
  }
}

const handleAddCart = () => {
  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }
  cartStore.addToCart(product.value.id, quantity.value, {
    productName: product.value.productName,
    mainImage: product.value.mainImage,
    price: product.value.price
  })
  message.success('已加入购物车')
}

const handleBuyNow = () => {
  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }
  cartStore.addToCart(product.value.id, 1, {
    productName: product.value.productName,
    mainImage: product.value.mainImage,
    price: product.value.price
  })
  const cartItem = cartStore.items.find((i) => i.productId === product.value.id)
  router.push({ path: '/mall/checkout', query: { cartItemId: cartItem?.id || '' } })
}

watch(() => route.params.id, () => {
  if (route.name === 'MallDetail') loadProduct()
})

onMounted(() => {
  loadProduct()
})
</script>

<style lang="less" scoped>
.mall-detail {
  padding: 24px;
  min-height: 100%;
}

.detail-breadcrumb {
  font-size: 14px;
  color: var(--gray-500);
  margin-bottom: 20px;

  a {
    color: var(--main-color, #1677ff);
    text-decoration: none;
    &:hover { text-decoration: underline; }
  }

  .sep {
    margin: 0 8px;
    color: var(--gray-300);
  }

  .current {
    color: var(--gray-700);
  }
}

.detail-main {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 32px;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  border: 1px solid var(--gray-100);
}

.detail-gallery {
  flex-shrink: 0;
}

.detail-img {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--gray-100);
  display: block;
}

.detail-info {
  min-width: 0;
}

.detail-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0 0 6px;
  line-height: 1.3;
}

.detail-brand {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0 0 12px;
}

.detail-price-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-price {
  font-size: 28px;
  font-weight: 700;
  color: #e85d2f;
}

.detail-desc {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.7;
  margin: 0 0 20px;
}

.detail-specs {
  margin-bottom: 24px;
}

.detail-actions {
  border-top: 1px solid var(--gray-100);
  padding-top: 20px;
}

.qty-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.qty-label {
  font-size: 14px;
  color: var(--gray-600);
}

.btn-row {
  display: flex;
  gap: 12px;
}

@media (max-width: 900px) {
  .detail-main {
    grid-template-columns: 1fr;
  }

  .detail-gallery {
    max-width: 360px;
  }
}

@media (max-width: 480px) {
  .btn-row {
    flex-direction: column;
  }
}
</style>
