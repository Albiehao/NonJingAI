<template>
  <div class="cart-page">
    <div class="cart-header">
      <h1 class="cart-title">购物车</h1>
      <p class="cart-subtitle">管理购物车中的商品，确认数量后结算</p>
    </div>

    <a-spin :spinning="false" tip="加载中...">
      <template v-if="cartStore.items.length">
        <div class="cart-card">
          <div class="cart-toolbar">
            <a-checkbox v-model:checked="isAllSelected" @change="handleSelectAll">全选</a-checkbox>
            <div class="toolbar-actions">
              <a-button
                  type="link"
                  danger
                  size="small"
                  :disabled="selectedIds.size === 0"
                  @click="handleDeleteSelected"
              >
                删除选中 ({{ selectedIds.size }})
              </a-button>
              <a-divider type="vertical" />
              <a-button type="link" danger size="small" @click="handleClear">清空购物车</a-button>
            </div>
          </div>

          <div class="cart-list">
            <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
              <a-checkbox
                  :checked="selectedIds.has(item.id)"
                  @change="(e) => handleSelect(item.id, e.target.checked)"
                  class="item-checkbox"
              />
              <img
                  :src="item.mainImage || '/img/001.jpeg'"
                  :alt="item.productName"
                  class="item-img"
              />
              <div class="item-info">
                <h3 class="item-name">{{ item.productName }}</h3>
                <span class="item-price">¥{{ formatPrice(item.price) }}</span>
              </div>
              <div class="item-qty">
                <a-button
                    size="small"
                    :disabled="item.quantity <= 1"
                    @click="handleChangeQty(item, item.quantity - 1)"
                >
                  <template #icon><MinusIcon :size="14" /></template>
                </a-button>
                <a-input-number
                    :value="item.quantity"
                    :min="1"
                    :max="99"
                    class="qty-input"
                    size="small"
                    @change="(val) => handleChangeQty(item, val)"
                />
                <a-button
                    size="small"
                    @click="handleChangeQty(item, item.quantity + 1)"
                >
                  <template #icon><PlusIcon :size="14" /></template>
                </a-button>
              </div>
              <div class="item-subtotal">¥{{ formatPrice(item.price * item.quantity) }}</div>
              <a-button
                  type="text"
                  danger
                  size="small"
                  class="item-delete"
                  @click="handleDelete(item)"
              >
                <template #icon><TrashIcon :size="16" /></template>
              </a-button>
            </div>
          </div>

          <div class="cart-footer">
            <div class="footer-left">
              <span class="selected-text">已选 <em>{{ selectedCount }}</em> 件商品</span>
              <span class="total-text">
                合计: <em>¥{{ formatPrice(totalPrice) }}</em>
              </span>
            </div>
            <a-button
                type="primary"
                size="large"
                :disabled="selectedCount === 0"
                @click="handleCheckout"
            >
              去结算
            </a-button>
          </div>
        </div>
      </template>

      <div v-else class="empty-state">
        <a-empty description="购物车空空如也">
          <a-button type="primary" @click="goMall">去逛逛</a-button>
        </a-empty>
      </div>
    </a-spin>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import { Minus as MinusIcon, Plus as PlusIcon, Trash2 as TrashIcon } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()


const selectedIds = ref(new Set())

const formatPrice = (price) => Number(price || 0).toFixed(2)

const selectedCount = computed(() => {
  let count = 0
  for (const id of selectedIds.value) {
    const item = cartStore.items.find((i) => i.id === id)
    if (item) count += item.quantity
  }
  return count
})

const totalPrice = computed(() => {
  let total = 0
  for (const id of selectedIds.value) {
    const item = cartStore.items.find((i) => i.id === id)
    if (item) total += item.price * item.quantity
  }
  return total
})

const isAllSelected = computed({
  get: () => cartStore.items.length > 0 && selectedIds.value.size === cartStore.items.length,
  set: () => {}
})

const handleChangeQty = (item, newQty) => {
  if (!newQty || newQty < 1 || newQty > 99) return
  cartStore.updateQuantity(item.id, newQty)
}

const handleDelete = (item) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除「${item.productName}」吗？`,
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: () => {
      cartStore.removeItem(item.id)
      selectedIds.value.delete(item.id)
      message.success('已删除')
    }
  })
}

const handleDeleteSelected = () => {
  if (selectedIds.value.size === 0) return
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除选中的 ${selectedIds.value.size} 件商品吗？`,
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: () => {
      for (const id of selectedIds.value) {
        cartStore.removeItem(id)
      }
      selectedIds.value.clear()
      message.success('已删除')
    }
  })
}

const handleClear = () => {
  Modal.confirm({
    title: '清空购物车',
    content: '确定要清空购物车中的所有商品吗？',
    okText: '清空',
    okType: 'danger',
    cancelText: '取消',
    onOk: () => {
      cartStore.clearCart()
      selectedIds.value.clear()
      message.success('购物车已清空')
    }
  })
}

const handleSelect = (id, checked) => {
  const newSet = new Set(selectedIds.value)
  if (checked) {
    newSet.add(id)
  } else {
    newSet.delete(id)
  }
  selectedIds.value = newSet
}

const handleSelectAll = () => {
  if (isAllSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(cartStore.items.map((i) => i.id))
  }
}

const handleCheckout = () => {
  if (selectedIds.value.size === 0) return
  const ids = [...selectedIds.value].join(',')
  router.push({ path: '/mall/checkout', query: { cartItemIds: ids } })
}

const goMall = () => {
  router.push('/mall')
}
</script>


<style lang="less" scoped>
.cart-page {
  padding: 24px;
  min-height: 100%;
}

.cart-header {
  margin-bottom: 20px;
}

.cart-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 6px;
}

.cart-subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

.cart-card {
  background: #fff;
  border-radius: 8px;
  border: 1px solid var(--gray-100);
  overflow: hidden;
}

.cart-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid var(--gray-100);
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.cart-list {
  padding: 0 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--gray-50);

  &:last-child {
    border-bottom: none;
  }
}

.item-checkbox {
  flex-shrink: 0;
}

.item-img {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid var(--gray-100);
  flex-shrink: 0;
  background: var(--gray-50, #f9fafb);
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  font-size: 14px;
  color: var(--gray-500);
}

.item-qty {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.qty-input {
  width: 56px;
}

.item-subtotal {
  font-size: 16px;
  font-weight: 700;
  color: #e85d2f;
  min-width: 80px;
  text-align: right;
  flex-shrink: 0;
}

.item-delete {
  flex-shrink: 0;
}

.cart-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-top: 1px solid var(--gray-100);
  background: var(--gray-50, #f9fafb);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.selected-text {
  font-size: 14px;
  color: var(--gray-600);

  em {
    font-style: normal;
    font-weight: 600;
    color: var(--gray-900);
  }
}

.total-text {
  font-size: 14px;
  color: var(--gray-600);

  em {
    font-style: normal;
    font-size: 22px;
    font-weight: 700;
    color: #e85d2f;
  }
}

.empty-state {
  background: #fff;
  border-radius: 8px;
  padding: 80px 0;
  text-align: center;
  border: 1px solid var(--gray-100);
}

@media (max-width: 768px) {
  .cart-item {
    flex-wrap: wrap;
    gap: 12px;
  }

  .item-info {
    flex-basis: calc(100% - 96px);
  }

  .item-subtotal {
    min-width: auto;
  }

  .cart-footer {
    flex-direction: column;
    gap: 12px;
  }
}
</style>