<script setup>
import { ref, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import {
  getCategories,
  getAgrochemicals, getAgrochemicalsByCategory, searchAgrochemicals,
  addAgrochemical, updateAgrochemical, deleteAgrochemical,
  getCrops, addCrop, updateCrop, deleteCrop,
  addCategory, updateCategory, deleteCategory,
  uploadFile,
  setCropToken, setCropUser, getCropToken, cropLogin
} from '@/apis/crop'

// ===== 状态 =====
const activeTab = ref('agrochemicals')
const agrochemicals = ref([])
const crops = ref([])
const categories = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const selectedCategoryId = ref(null)

// 农资弹窗
const agroModalVisible = ref(false)
const agroEditing = ref(null)
const agroForm = ref({})
const agroImageFile = ref(null)
const agroImagePreview = ref('')

// 作物弹窗
const cropModalVisible = ref(false)
const cropEditing = ref(null)
const cropForm = ref({})

// 分类弹窗
const categoryModalVisible = ref(false)
const categoryEditing = ref(null)
const categoryForm = ref({})

// ===== 数据加载 =====
async function loadCategories() {
  try {
    const res = await getCategories()
    if (res.code === 0) categories.value = res.data
  } catch (e) { console.error(e) }
}

async function loadAgrochemicals() {
  loading.value = true
  try {
    let res
    if (selectedCategoryId.value) {
      res = await getAgrochemicalsByCategory(selectedCategoryId.value)
    } else if (searchKeyword.value) {
      res = await searchAgrochemicals(searchKeyword.value)
    } else {
      res = await getAgrochemicals()
    }
    if (res.code === 0) agrochemicals.value = res.data || []
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function loadCrops() {
  loading.value = true
  try {
    const res = await getCrops()
    if (res.code === 0) crops.value = res.data || []
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}


function getCategoryName(id) {
  const c = categories.value.find(c => c.id === id)
  return c ? c.name : '-'
}

async function ensureLoggedIn() {
  if (!getCropToken()) {
    try {
      const res = await cropLogin('cropadmin', 'admin123')
      if (res.code === 0) {
        setCropToken(res.data.token)
        setCropUser(res.data)
      } else {
        message.error('农资系统登录失败')
      }
    } catch (e) {
      console.error('农资系统自动登录失败', e)
    }
  }
}

onMounted(async () => {
  await ensureLoggedIn()
  loadCategories()
  loadAgrochemicals()
  loadCrops()
})

// ===== 搜索/筛选 =====
function handleSearch() {
  selectedCategoryId.value = null
  loadAgrochemicals()
}

function handleCategoryFilter(categoryId) {
  selectedCategoryId.value = categoryId
  searchKeyword.value = ''
  loadAgrochemicals()
}

// ===== 农资 CRUD =====
function openAgroAdd() {
  agroEditing.value = null
  agroForm.value = { productName: '', brand: '', price: 0, monthlySales: 0, categoryId: null, description: '', registrationNo: '', formulation: '', contentSpec: '', useCrops: '', usageMethod: '', precautions: '', purchaseLinks: '' }
  agroImageFile.value = null
  agroImagePreview.value = ''
  agroModalVisible.value = true
}

function openAgroEdit(item) {
  agroEditing.value = item
  agroForm.value = { ...item }
  agroImageFile.value = null
  agroImagePreview.value = item.mainImage || ''
  agroModalVisible.value = true
}

async function saveAgrochemical() {
  try {
    // 先上传图片（如果有选择新图片）
    if (agroImageFile.value) {
      const uploadRes = await uploadFile(agroImageFile.value, 'crop-images')
      if (uploadRes.code === 0) {
        agroForm.value.mainImage = uploadRes.data
      } else {
        message.error('图片上传失败')
        return
      }
    }

    const data = { ...agroForm.value }
    if (data.price !== undefined && data.price !== null) {
      data.price = Number(data.price)
    }
    if (data.monthlySales !== undefined && data.monthlySales !== null) {
      data.monthlySales = Number(data.monthlySales)
    }
    const res = agroEditing.value
      ? await updateAgrochemical(data)
      : await addAgrochemical(data)
    if (res.code === 0) {
      message.success(agroEditing.value ? '修改成功' : '添加成功')
      agroModalVisible.value = false
      loadAgrochemicals()
    } else {
      message.error(res.message || '操作失败')
    }
  } catch (e) {
    console.error('saveAgrochemical error:', e)
    message.error('网络异常: ' + (e.message || ''))
  }
}

async function handleDeleteAgro(id) {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除该农资商品吗？',
    onOk: async () => {
      try {
        const res = await deleteAgrochemical(id)
        if (res.code === 0) {
          message.success('删除成功')
          loadAgrochemicals()
        } else {
          message.error(res.message || '删除失败')
        }
      } catch (e) {
        message.error('网络异常')
      }
    }
  })
}

// ===== 作物 CRUD =====
function openCropAdd() {
  cropEditing.value = null
  cropForm.value = { name: '', scientificName: '' }
  cropModalVisible.value = true
}

function openCropEdit(item) {
  cropEditing.value = item
  cropForm.value = { name: item.name, scientificName: item.scientificName || '' }
  cropModalVisible.value = true
}

async function saveCrop() {
  try {
    const res = cropEditing.value
      ? await updateCrop(cropEditing.value.id, cropForm.value.name, cropForm.value.scientificName)
      : await addCrop(cropForm.value.name, cropForm.value.scientificName)
    if (res.code === 0) {
      message.success(cropEditing.value ? '修改成功' : '添加成功')
      cropModalVisible.value = false
      loadCrops()
    } else {
      message.error(res.message || '操作失败')
    }
  } catch (e) {
    message.error('网络异常')
  }
}

async function handleDeleteCrop(id) {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除该作物吗？',
    onOk: async () => {
      try {
        const res = await deleteCrop(id)
        if (res.code === 0) {
          message.success('删除成功')
          loadCrops()
        } else {
          message.error(res.message || '删除失败')
        }
      } catch (e) {
        message.error('网络异常')
      }
    }
  })
}

// ===== 分类 CRUD =====
function openCategoryAdd() {
  categoryEditing.value = null
  categoryForm.value = { name: '', description: '' }
  categoryModalVisible.value = true
}

function openCategoryEdit(item) {
  categoryEditing.value = item
  categoryForm.value = { name: item.name, description: item.description || '' }
  categoryModalVisible.value = true
}

async function saveCategory() {
  try {
    const res = categoryEditing.value
      ? await updateCategory(categoryEditing.value.id, categoryForm.value.name, null, categoryForm.value.description)
      : await addCategory(categoryForm.value.name, null, categoryForm.value.description)
    if (res.code === 0) {
      message.success(categoryEditing.value ? '修改成功' : '添加成功')
      categoryModalVisible.value = false
      loadCategories()
    } else {
      message.error(res.message || '操作失败')
    }
  } catch (e) {
    message.error('网络异常')
  }
}

async function handleDeleteCategory(id) {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除该分类吗？',
    onOk: async () => {
      try {
        const res = await deleteCategory(id)
        if (res.code === 0) {
          message.success('删除成功')
          loadCategories()
        } else {
          message.error(res.message || '删除失败')
        }
      } catch (e) {
        message.error('网络异常')
      }
    }
  })
}

</script>

<template>
  <div class="crop-admin">
    <h2 style="margin:0 0 16px 0;font-size:20px;">农资管理</h2>

    <a-tabs v-model:activeKey="activeTab" type="card">
      <!-- 分类管理 -->
      <a-tab-pane key="categories" tab="分类管理">
        <div class="section-actions">
          <a-button type="primary" @click="openCategoryAdd">新增分类</a-button>
        </div>
        <a-table
          :dataSource="categories"
          rowKey="id"
          :pagination="{ pageSize: 20 }"
          size="small"
        >
          <a-table-column title="名称" dataIndex="name" :width="200" />
          <a-table-column title="描述" dataIndex="description" ellipsis />
          <a-table-column title="操作" :width="160" align="center">
            <template #default="{ record }">
              <a-space>
                <a-button size="small" type="primary" ghost @click="openCategoryEdit(record)">编辑</a-button>
                <a-button size="small" danger @click="handleDeleteCategory(record.id)">删除</a-button>
              </a-space>
            </template>
          </a-table-column>
        </a-table>
      </a-tab-pane>

      <!-- 农资管理 -->
      <a-tab-pane key="agrochemicals" tab="农资管理">
        <div class="section-actions">
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索品名/品牌"
            style="width: 280px"
            @search="handleSearch"
          />
          <a-button type="primary" @click="openAgroAdd">新增农资</a-button>
        </div>
        <div class="category-tags">
          <a-tag
            :color="selectedCategoryId === null ? 'blue' : 'default'"
            style="cursor:pointer"
            @click="handleCategoryFilter(null)"
          >
            全部
          </a-tag>
          <a-tag
            v-for="c in categories"
            :key="c.id"
            :color="selectedCategoryId === c.id ? 'blue' : 'default'"
            style="cursor:pointer"
            @click="handleCategoryFilter(c.id)"
          >
            {{ c.name }}
          </a-tag>
        </div>
        <a-table
          :dataSource="agrochemicals"
          :loading="loading"
          rowKey="id"
          :pagination="{ pageSize: 15 }"
          size="small"
        >
          <a-table-column title="图片" :width="120">
            <template #default="{ record }">
              <div style="display:flex;justify-content:center;">
                <img v-if="record.mainImage" :src="record.mainImage" style="width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid #f0f0f0;box-shadow:0 2px 6px rgba(0,0,0,0.06);" @error="$event.target.style.display='none'" />
                <span v-else style="color:#bbb;font-size:12px;">无图片</span>
              </div>
            </template>
          </a-table-column>
          <a-table-column title="品名" dataIndex="productName" :width="160" ellipsis />
          <a-table-column title="品牌" dataIndex="brand" :width="120" ellipsis />
          <a-table-column title="分类" :width="100">
            <template #default="{ record }">
              {{ getCategoryName(record.categoryId) }}
            </template>
          </a-table-column>
          <a-table-column title="价格(元)" dataIndex="price" :width="100">
            <template #default="{ record }">
              {{ record.price ? (record.price / 100).toFixed(2) : '-' }}
            </template>
          </a-table-column>
          <a-table-column title="月销量" dataIndex="monthlySales" :width="80" />
          <a-table-column title="购买链接" :width="200" ellipsis>
            <template #default="{ record }">
              <a v-if="record.purchaseLinks" :href="record.purchaseLinks" target="_blank" style="font-size:12px;">{{ record.purchaseLinks }}</a>
              <span v-else style="color:#bbb;">-</span>
            </template>
          </a-table-column>
          <a-table-column title="操作" :width="160" align="center">
            <template #default="{ record }">
              <a-space>
                <a-button size="small" type="primary" ghost @click="openAgroEdit(record)">编辑</a-button>
                <a-button size="small" danger @click="handleDeleteAgro(record.id)">删除</a-button>
              </a-space>
            </template>
          </a-table-column>
        </a-table>
      </a-tab-pane>

      <!-- 作物管理 -->
      <a-tab-pane key="crops" tab="作物管理">
        <div class="section-actions">
          <a-button type="primary" @click="openCropAdd">新增作物</a-button>
        </div>
        <a-table
          :dataSource="crops"
          :loading="loading"
          rowKey="id"
          :pagination="{ pageSize: 20 }"
          size="small"
        >
          <a-table-column title="名称" dataIndex="name" />
          <a-table-column title="学名" dataIndex="scientificName" />
          <a-table-column title="操作" :width="160" align="center">
            <template #default="{ record }">
              <a-space>
                <a-button size="small" type="primary" ghost @click="openCropEdit(record)">编辑</a-button>
                <a-button size="small" danger @click="handleDeleteCrop(record.id)">删除</a-button>
              </a-space>
            </template>
          </a-table-column>
        </a-table>
      </a-tab-pane>
    </a-tabs>

    <!-- 农资弹窗 -->
    <a-modal
      v-model:open="agroModalVisible"
      :title="agroEditing ? '编辑农资' : '新增农资'"
      :width="720"
      @ok="saveAgrochemical"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form layout="vertical">
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="品名" required>
              <a-input v-model:value="agroForm.productName" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="品牌">
              <a-input v-model:value="agroForm.brand" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="24">
          <a-col :span="8">
            <a-form-item label="分类">
              <a-select v-model:value="agroForm.categoryId" allowClear placeholder="选择分类">
                <a-select-option v-for="c in categories" :key="c.id" :value="c.id">
                  {{ c.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="价格(元)">
              <a-input-number
                v-model:value="agroForm.price"
                style="width:100%"
                :precision="2"
                :formatter="v => v !== undefined ? (Number(v) / 100).toFixed(2) : '0.00'"
                :parser="v => v ? String(Math.round(parseFloat(v) * 100)) : '0'"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="月销量">
              <a-input-number v-model:value="agroForm.monthlySales" style="width:100%" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="图片">
          <div style="display:flex;align-items:center;gap:12px;">
            <img v-if="agroImagePreview" :src="agroImagePreview" style="width:100px;height:100px;object-fit:cover;border-radius:8px;border:1px solid #d9d9d9;box-shadow:0 2px 8px rgba(0,0,0,0.08);" @error="$event.target.style.display='none'" />
            <a-upload :before-upload="(file) => { agroImageFile.value = file; agroImagePreview.value = URL.createObjectURL(file); return false }" :show-upload-list="false" accept="image/*">
              <a-button>{{ agroImagePreview ? '换图' : '选择图片' }}</a-button>
            </a-upload>
          </div>
        </a-form-item>
        <a-row :gutter="24">
          <a-col :span="8">
            <a-form-item label="登记证号">
              <a-input v-model:value="agroForm.registrationNo" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="剂型">
              <a-input v-model:value="agroForm.formulation" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="规格">
              <a-input v-model:value="agroForm.contentSpec" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="适用作物">
          <a-input v-model:value="agroForm.useCrops" />
        </a-form-item>
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="使用方法">
              <a-textarea v-model:value="agroForm.usageMethod" :rows="2" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="注意事项">
              <a-textarea v-model:value="agroForm.precautions" :rows="2" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="描述">
          <a-textarea v-model:value="agroForm.description" :rows="2" />
        </a-form-item>
        <a-form-item label="购买链接">
          <a-input v-model:value="agroForm.purchaseLinks" placeholder="https://" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 作物弹窗 -->
    <a-modal
      v-model:open="cropModalVisible"
      :title="cropEditing ? '编辑作物' : '新增作物'"
      @ok="saveCrop"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form layout="vertical">
        <a-form-item label="名称" required>
          <a-input v-model:value="cropForm.name" />
        </a-form-item>
        <a-form-item label="学名">
          <a-input v-model:value="cropForm.scientificName" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 分类弹窗 -->
    <a-modal
      v-model:open="categoryModalVisible"
      :title="categoryEditing ? '编辑分类' : '新增分类'"
      @ok="saveCategory"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form layout="vertical">
        <a-form-item label="名称" required>
          <a-input v-model:value="categoryForm.name" />
        </a-form-item>
        <a-form-item label="描述">
          <a-textarea v-model:value="categoryForm.description" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.crop-admin {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}
.section-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: center;
}
.category-tags {
  margin-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 16px;
}
</style>
