<template>
  <section class="admin-panel">
    <div class="admin-panel-head">
      <h3 class="admin-panel-title">农资商品管理</h3>
      <button type="button" class="admin-btn" @click="openCreate">新增农资商品</button>
    </div>
    <admin-table-scroll>
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>图片</th>
            <th>商品名称</th>
            <th>商品分类</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in products" :key="item.id">
            <td>{{ item.id }}</td>
            <td class="img-cell">
              <img class="product-thumb" :src="item.mainImage || fallbackImage" :alt="item.productName" />
            </td>
            <td>{{ item.productName }}</td>
            <td>{{ categoryName(item.categoryId) }}</td>
            <td>
              <button type="button" class="admin-btn" @click="openDetail(item)">查看详情</button>
              <button type="button" class="admin-btn" @click="openEdit(item)">编辑</button>
              <button type="button" class="admin-btn danger" @click="$emit('remove', item.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </admin-table-scroll>

    <div v-if="editingProduct" class="admin-modal-mask" @click.self="closeEdit">
      <div class="admin-modal">
        <h4 class="admin-modal-title">编辑商品</h4>
        <div class="admin-form-grid">
          <label class="admin-modal-field">
            <span>分类</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="editCategoryMenuOpen = !editCategoryMenuOpen">
                {{ categoryName(form.categoryId) }}
              </button>
              <ul v-if="editCategoryMenuOpen" class="admin-select-menu">
                <li v-for="c in categories" :key="c.id" @click="setEditCategory(c.id)">{{ c.name }}</li>
              </ul>
            </div>
          </label>
          <label class="admin-modal-field">
            <span>图片 URL</span>
            <input v-model.trim="form.mainImage" type="url" placeholder="如 https://... 或 /img/003.jpeg" />
          </label>
          <label class="admin-modal-field span-2">
            <span>商品全称</span>
            <input v-model.trim="form.productName" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>生产厂家</span>
            <input v-model.trim="form.manufacturer" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>农药登记证号</span>
            <input v-model.trim="form.registrationNo" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>剂型</span>
            <input v-model.trim="form.formulation" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>含量规格</span>
            <input v-model.trim="form.contentSpec" type="text" />
          </label>
          <label class="admin-modal-field span-2">
            <span>适用农作物</span>
            <input v-model.trim="form.useCrops" type="text" />
          </label>
          <label class="admin-modal-field span-2">
            <span>购买链接</span>
            <input v-model.trim="form.purchaseLinks" type="text" />
          </label>
        </div>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="saveEdit">保存</button>
          <button type="button" class="admin-btn danger" @click="closeEdit">取消</button>
        </div>
      </div>
    </div>
    <div v-if="detailProduct" class="admin-modal-mask" @click.self="closeDetail">
      <div class="admin-modal admin-modal--detail">
        <h4 class="admin-modal-title">商品详情</h4>
        <div class="detail-hero">
          <img class="detail-img" :src="detailProduct.mainImage || fallbackImage" :alt="detailProduct.productName" />
          <div class="detail-hero-text">
            <p class="detail-name">{{ detailProduct.productName }}</p>
            <p class="detail-sub">{{ categoryName(detailProduct.categoryId) }}</p>
          </div>
        </div>
        <div class="detail-grid">
          <div class="detail-item"><span class="k">ID</span><span class="v">{{ detailProduct.id }}</span></div>
          <div class="detail-item"><span class="k">分类</span><span class="v">{{ categoryName(detailProduct.categoryId) }}</span></div>
          <div class="detail-item"><span class="k">生产厂家</span><span class="v">{{ detailProduct.manufacturer || '-' }}</span></div>
          <div class="detail-item"><span class="k">登记证号</span><span class="v">{{ detailProduct.registrationNo || '-' }}</span></div>
          <div class="detail-item"><span class="k">剂型</span><span class="v">{{ detailProduct.formulation || '-' }}</span></div>
          <div class="detail-item"><span class="k">含量规格</span><span class="v">{{ detailProduct.contentSpec || '-' }}</span></div>
          <div class="detail-item"><span class="k">适用作物</span><span class="v">{{ detailProduct.useCrops || '-' }}</span></div>
          <div class="detail-item"><span class="k">购买链接</span><span class="v">{{ detailProduct.purchaseLinks || '-' }}</span></div>
          <div class="detail-item"><span class="k">更新时间</span><span class="v">{{ detailProduct.updatedAt || '-' }}</span></div>
          <div class="detail-item"><span class="k">图片 URL</span><span class="v">{{ detailProduct.mainImage || '-' }}</span></div>
        </div>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="closeDetail">关闭</button>
        </div>
      </div>
    </div>
    <div v-if="creatingProduct" class="admin-modal-mask" @click.self="closeCreate">
      <div class="admin-modal">
        <h4 class="admin-modal-title">新增商品</h4>
        <label class="admin-modal-field">
          <span>分类</span>
          <div class="admin-pseudo-select">
            <button type="button" class="admin-select-trigger" @click="createCategoryMenuOpen = !createCategoryMenuOpen">
              {{ categoryName(createForm.categoryId) }}
            </button>
            <ul v-if="createCategoryMenuOpen" class="admin-select-menu">
              <li v-for="c in categories" :key="c.id" @click="setCreateCategory(c.id)">{{ c.name }}</li>
            </ul>
          </div>
        </label>
        <label class="admin-modal-field">
          <span>图片 URL</span>
          <input v-model.trim="createForm.mainImage" type="url" placeholder="如 https://... 或 /img/003.jpeg" />
        </label>
        <label class="admin-modal-field">
          <span>商品全称</span>
          <input v-model.trim="createForm.productName" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>生产厂家</span>
          <input v-model.trim="createForm.manufacturer" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>农药登记证号</span>
          <input v-model.trim="createForm.registrationNo" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>剂型</span>
          <input v-model.trim="createForm.formulation" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>含量规格</span>
          <input v-model.trim="createForm.contentSpec" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>适用农作物</span>
          <input v-model.trim="createForm.useCrops" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>购买链接</span>
          <input v-model.trim="createForm.purchaseLinks" type="text" />
        </label>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="saveCreate">确认新增</button>
          <button type="button" class="admin-btn danger" @click="closeCreate">取消</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import AdminTableScroll from './AdminTableScroll.vue'

export default {
  name: 'AdminProducts',
  components: {
    AdminTableScroll
  },
  props: {
    products: {
      type: Array,
      default: () => []
    },
    categories: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingProduct: null,
      creatingProduct: false,
      detailProduct: null,
      fallbackImage: '/img/003.jpeg',
      editCategoryMenuOpen: false,
      createCategoryMenuOpen: false,
      form: {
        categoryId: 1,
        mainImage: '',
        productName: '',
        manufacturer: '',
        registrationNo: '',
        formulation: '',
        contentSpec: '',
        useCrops: '',
        purchaseLinks: ''
      },
      createForm: {
        categoryId: 1,
        mainImage: '',
        productName: '',
        manufacturer: '',
        registrationNo: '',
        formulation: '',
        contentSpec: '',
        useCrops: '',
        purchaseLinks: ''
      }
    }
  },
  methods: {
    categoryName(categoryId) {
      const id = Number(categoryId)
      const found = this.categories.find(c => Number(c.id) === id)
      return found ? found.name : `未知分类(${categoryId})`
    },
    openEdit(product) {
      this.editingProduct = product
      this.form = {
        categoryId: product.categoryId,
        mainImage: product.mainImage || '',
        productName: product.productName,
        manufacturer: product.manufacturer || '',
        registrationNo: product.registrationNo || '',
        formulation: product.formulation || '',
        contentSpec: product.contentSpec || '',
        useCrops: product.useCrops || '',
        purchaseLinks: product.purchaseLinks || ''
      }
      this.editCategoryMenuOpen = false
    },
    openCreate() {
      this.creatingProduct = true
      this.createForm = {
        categoryId: this.categories[0] ? this.categories[0].id : 1,
        mainImage: '',
        productName: '',
        manufacturer: '',
        registrationNo: '',
        formulation: '',
        contentSpec: '',
        useCrops: '',
        purchaseLinks: ''
      }
      this.createCategoryMenuOpen = false
    },
    closeCreate() {
      this.creatingProduct = false
      this.createCategoryMenuOpen = false
    },
    saveCreate() {
      const productName = this.createForm.productName.trim()
      const categoryId = Number(this.createForm.categoryId)
      if (!productName || !Number.isFinite(categoryId) || categoryId <= 0) return
      this.$emit('add', {
        categoryId,
        mainImage: this.createForm.mainImage.trim(),
        productName,
        manufacturer: this.createForm.manufacturer.trim(),
        registrationNo: this.createForm.registrationNo.trim(),
        formulation: this.createForm.formulation.trim(),
        contentSpec: this.createForm.contentSpec.trim(),
        useCrops: this.createForm.useCrops.trim(),
        purchaseLinks: this.createForm.purchaseLinks.trim(),
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeCreate()
    },
    closeEdit() {
      this.editingProduct = null
      this.editCategoryMenuOpen = false
    },
    setEditCategory(id) {
      this.form.categoryId = Number(id)
      this.editCategoryMenuOpen = false
    },
    setCreateCategory(id) {
      this.createForm.categoryId = Number(id)
      this.createCategoryMenuOpen = false
    },
    saveEdit() {
      if (!this.editingProduct) return
      const productName = this.form.productName.trim()
      const categoryId = Number(this.form.categoryId)
      if (!productName || !Number.isFinite(categoryId) || categoryId <= 0) return
      this.$emit('edit', {
        id: this.editingProduct.id,
        categoryId,
        mainImage: this.form.mainImage.trim(),
        productName,
        manufacturer: this.form.manufacturer.trim(),
        registrationNo: this.form.registrationNo.trim(),
        formulation: this.form.formulation.trim(),
        contentSpec: this.form.contentSpec.trim(),
        useCrops: this.form.useCrops.trim(),
        purchaseLinks: this.form.purchaseLinks.trim(),
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeEdit()
    },
    openDetail(product) {
      this.detailProduct = product
    },
    closeDetail() {
      this.detailProduct = null
    }
  }
}
</script>

<style scoped>
.img-cell {
  width: 124px;
}

.product-thumb {
  width: 96px;
  height: 96px;
  object-fit: cover;
  display: block;
  border: 2px solid #2a1c12;
  background: #1d2431;
}

.admin-modal--detail {
  width: min(720px, calc(100vw - 24px));
}

.detail-hero {
  margin-top: 12px;
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 12px;
  align-items: center;
  border: 2px solid rgba(42, 28, 18, 0.65);
  background: rgba(0, 0, 0, 0.12);
  padding: 12px;
}

.detail-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  display: block;
  border: 2px solid #2a1c12;
  background: #1d2431;
}

.admin-form-grid {
  margin-top: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 12px;
}

.admin-form-grid .admin-modal-field {
  margin-top: 0;
}

.admin-form-grid .admin-modal-field.span-2 {
  grid-column: 1 / -1;
}

.detail-name {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #f5e6cc;
}

.detail-sub {
  margin-top: 6px;
  font-size: 12px;
  color: rgba(245, 230, 204, 0.78);
  letter-spacing: 1px;
}

.detail-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 14px;
}

.detail-item {
  border: 2px solid rgba(42, 28, 18, 0.55);
  background: rgba(0, 0, 0, 0.08);
  padding: 10px 12px;
  display: flex;
  gap: 10px;
  align-items: baseline;
  min-width: 0;
}

.detail-item .k {
  flex: 0 0 64px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #f5e6cc;
}

.detail-item .v {
  font-size: 12px;
  color: rgba(245, 230, 204, 0.9);
  word-break: break-all;
}

.admin-pseudo-select {
  position: relative;
}

.admin-select-trigger {
  width: 100%;
  text-align: left;
  border: 2px solid #2a1c12;
  background: #2b3038;
  color: #f5e6cc;
  padding: 12px 36px 12px 14px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  cursor: pointer;
  outline: none;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
  position: relative;
}

.admin-select-trigger::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  width: 10px;
  height: 10px;
  transform: translateY(-50%) rotate(45deg);
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
}

.admin-select-menu {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  border: 2px solid #2a1c12;
  background: #2b3038;
  box-shadow: 0 6px 0 rgba(0, 0, 0, 0.28);
  z-index: 6;
  max-height: 240px;
  overflow: auto;
}

.admin-select-menu li {
  padding: 10px 12px;
  cursor: pointer;
  color: #f5e6cc;
}

.admin-select-menu li:hover {
  background: #333a45;
}
.admin-modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(12, 14, 22, 0.58);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 80;
}

.admin-modal {
  width: min(440px, calc(100vw - 24px));
  border: 2px solid #2a1c12;
  background: #252c3a;
  box-shadow: 0 12px 0 rgba(0, 0, 0, 0.32);
  padding: 16px;
}

.admin-modal-title {
  color: #f5e6cc;
  font-size: 13px;
  letter-spacing: 1px;
}

.admin-modal-field {
  display: block;
  margin-top: 10px;
}

.admin-modal-field span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: bold;
  color: #f5e6cc;
  letter-spacing: 1px;
}

.admin-modal-field input {
  width: 100%;
  box-sizing: border-box;
  border: 2px solid #2a1c12;
  background: #2b3038;
  color: #f5e6cc;
  padding: 12px 14px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.admin-modal-field input:focus {
  border-color: #8d6b4b;
  background: #333a45;
  box-shadow:
    0 0 0 2px rgba(141, 107, 75, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.admin-modal-field input::placeholder {
  color: #8e98a8;
}

.admin-modal-actions {
  margin-top: 14px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.admin-modal-actions .admin-btn {
  min-width: 74px;
}

.admin-page.light-mode .admin-modal {
  background: #e8dece;
}

.admin-page.light-mode .admin-modal-title,
.admin-page.light-mode .admin-modal-field span {
  color: #4b3a2b;
  text-shadow: none;
}

.admin-page.light-mode .admin-modal-field input {
  background: #f1e9db;
  color: #433224;
  border-color: #8d6b4b;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.admin-page.light-mode .admin-modal-field input:focus {
  background: #ece1d0;
  border-color: #6f4c30;
  box-shadow:
    0 0 0 2px rgba(111, 76, 48, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.admin-page.light-mode .admin-select-trigger {
  background: #f1e9db;
  color: #433224;
  border-color: #8d6b4b;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
}

.admin-page.light-mode .admin-select-menu {
  background: #f1e9db;
  border-color: #8d6b4b;
}

.admin-page.light-mode .admin-select-menu li {
  color: #433224;
}

.admin-page.light-mode .admin-select-menu li:hover {
  background: #ece1d0;
}

.admin-page.light-mode .detail-name,
.admin-page.light-mode .detail-item .k {
  color: #4b3a2b;
}

.admin-page.light-mode .detail-sub,
.admin-page.light-mode .detail-item .v {
  color: rgba(75, 58, 43, 0.9);
}
</style>

