<template>
  <BaseToolCall :tool-call="toolCall" :hide-params="true" default-expanded>
    <template #header>
      <div class="sep-header">
        <span class="note">农资查询</span>
        <span class="separator" v-if="searchKeyword">|</span>
        <span class="description">{{ searchKeyword }}</span>
      </div>
    </template>
    <template #result="{ resultContent }">
      <div class="agrochemicals-result">
        <!-- 单个产品详情 -->
        <div class="product-detail" v-if="productDetail">
          <div class="product-card">
            <img v-if="productDetail.main_image" :src="productDetail.main_image" class="product-image" @error="$event.target.style.display='none'" />
            <div class="product-header">
              <h4 class="product-name">{{ productDetail.product_name }}</h4>
              <span class="product-brand" v-if="productDetail.brand">{{ productDetail.brand }}</span>
            </div>
            <div class="product-price" v-if="productDetail.price">
              ¥{{ productDetail.price }}
            </div>
            <div class="product-links" v-if="productDetail.purchase_links">
              <a :href="productDetail.purchase_links" target="_blank" class="buy-link">查看购买渠道 →</a>
            </div>
            <div class="product-specs">
              <div class="spec-item" v-if="productDetail.formulation">
                <span class="spec-label">剂型</span>
                <span class="spec-value">{{ productDetail.formulation }}</span>
              </div>
              <div class="spec-item" v-if="productDetail.content_spec">
                <span class="spec-label">规格</span>
                <span class="spec-value">{{ productDetail.content_spec }}</span>
              </div>
              <div class="spec-item" v-if="productDetail.registration_no">
                <span class="spec-label">登记证号</span>
                <span class="spec-value">{{ productDetail.registration_no }}</span>
              </div>
            </div>
            <div class="product-section" v-if="productDetail.use_crops">
              <div class="section-label">适用作物</div>
              <div class="section-content">{{ productDetail.use_crops }}</div>
            </div>
            <div class="product-section" v-if="productDetail.usage_method">
              <div class="section-label">使用方法</div>
              <div class="section-content">{{ productDetail.usage_method }}</div>
            </div>
            <div class="product-section warning" v-if="productDetail.precautions">
              <div class="section-label">注意事项</div>
              <div class="section-content">{{ productDetail.precautions }}</div>
            </div>
          </div>
        </div>

        <!-- 产品列表 -->
        <div class="products-list" v-else-if="products.length > 0">
          <div class="list-header">
            <span class="count-badge">共 {{ products.length }} 个产品</span>
          </div>
          <div class="products-grid">
            <div v-for="product in products" :key="product.id" class="product-card mini">
              <div class="card-header">
                <h5 class="card-title">{{ product.product_name }}</h5>
                <span class="card-brand" v-if="product.brand">{{ product.brand }}</span>
              </div>
              <div class="card-body">
                <div class="card-price" v-if="product.price">¥{{ product.price }}</div>
                <div class="card-info" v-if="product.formulation">{{ product.formulation }}</div>
                <div class="card-crops" v-if="product.use_crops">
                  <span class="crop-label">适用：</span>
                  <span class="crop-value">{{ truncateText(product.use_crops, 30) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 分类列表 -->
        <div class="categories-list" v-else-if="categories.length > 0">
          <div class="list-header">
            <span class="count-badge">共 {{ categories.length }} 个分类</span>
          </div>
          <div class="categories-grid">
            <div v-for="category in categories" :key="category.id" class="category-card">
              <span class="category-name">{{ category.name }}</span>
            </div>
          </div>
        </div>

        <!-- 无结果 -->
        <div v-else-if="parsedResult.message" class="no-results">
          <p>{{ parsedResult.message }}</p>
        </div>

        <!-- 错误 -->
        <div v-else-if="parsedResult.error" class="error-result">
          <p>{{ parsedResult.error }}</p>
        </div>
      </div>
    </template>
  </BaseToolCall>
</template>

<script setup>
import BaseToolCall from '../BaseToolCall.vue'
import { computed } from 'vue'

const props = defineProps({
  toolCall: {
    type: Object,
    required: true
  }
})

const parseData = (content) => {
  if (typeof content === 'string') {
    try {
      return JSON.parse(content)
    } catch (error) {
      return { error: '数据解析失败' }
    }
  }
  return content || {}
}

const parsedResult = computed(() => {
  const content = props.toolCall.tool_call_result?.content
  return parseData(content)
})

const toolName = computed(() => {
  return props.toolCall.name || props.toolCall.function?.name || ''
})

const searchKeyword = computed(() => {
  const args = props.toolCall.args || props.toolCall.function?.arguments
  if (!args) return ''
  if (typeof args === 'object') return args.keyword || args.product_name || args.agrochemical_id || args.category_id || ''
  try {
    const parsed = JSON.parse(args)
    return parsed.keyword || parsed.product_name || parsed.agrochemical_id || parsed.category_id || ''
  } catch {
    return ''
  }
})

// 单个产品详情
const productDetail = computed(() => {
  if (parsedResult.value.product_name && (toolName.value.includes('agrochemical') || toolName.value.includes('农资'))) {
    return parsedResult.value
  }
  return null
})

// 产品列表
const products = computed(() => {
  if (parsedResult.value.products && Array.isArray(parsedResult.value.products)) {
    return parsedResult.value.products
  }
  return []
})

// 分类列表
const categories = computed(() => {
  if (parsedResult.value.categories && Array.isArray(parsedResult.value.categories)) {
    return parsedResult.value.categories
  }
  return []
})

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}
</script>

<style lang="less" scoped>
.agrochemicals-result {
  background: var(--gray-0);
  border-radius: 8px;
  padding: 12px;
}

.list-header {
  margin-bottom: 12px;
}

.count-badge {
  font-size: 12px;
  color: var(--gray-600);
  background: var(--gray-100);
  padding: 4px 8px;
  border-radius: 4px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.categories-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.product-card {
  background: var(--gray-50);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--gray-200);

  .product-image {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 12px;
  }

  &.mini {
    padding: 12px;
  }

  .product-header,
  .card-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 12px;
  }

  .product-name,
  .card-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--gray-900);
    margin: 0;
  }

  .product-brand,
  .card-brand {
    font-size: 12px;
    color: var(--main-color);
  }

  .product-price,
  .card-price {
    font-size: 18px;
    font-weight: 600;
    color: #f56c6c;
    margin-bottom: 12px;
  }

  .product-links {
    margin-bottom: 12px;

    .buy-link {
      display: inline-block;
      font-size: 13px;
      color: var(--main-color);
      text-decoration: none;
      padding: 4px 12px;
      border: 1px solid var(--main-color);
      border-radius: 4px;
      transition: all 0.2s;

      &:hover {
        background: var(--main-color);
        color: #fff;
      }
    }
  }

  .card-price {
    font-size: 14px;
  }

  .product-specs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;

    .spec-item {
      display: flex;
      gap: 4px;
      font-size: 12px;

      .spec-label {
        color: var(--gray-500);
      }

      .spec-value {
        color: var(--gray-700);
      }
    }
  }

  .card-info {
    font-size: 12px;
    color: var(--gray-600);
    margin-bottom: 8px;
  }

  .card-crops {
    font-size: 12px;

    .crop-label {
      color: var(--gray-500);
    }

    .crop-value {
      color: var(--gray-700);
    }
  }

  .product-section {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--gray-200);

    .section-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--gray-600);
      margin-bottom: 6px;
    }

    .section-content {
      font-size: 13px;
      line-height: 1.6;
      color: var(--gray-800);
      white-space: pre-wrap;
    }

    &.warning {
      .section-label {
        color: #e6a23c;
      }
    }
  }
}

.category-card {
  background: var(--gray-100);
  border-radius: 6px;
  padding: 8px 16px;

  .category-name {
    font-size: 14px;
    color: var(--gray-700);
  }
}

.no-results,
.error-result {
  text-align: center;
  color: var(--gray-500);
  padding: 20px;
  font-size: 13px;
}

.error-result {
  color: #f56c6c;
}
</style>