<template>
  <div class="crop-dict-view">
    <div class="page-header">
      <h2>农作物字典</h2>
      <a-button type="primary" @click="openCropAdd" size="small">
        <template #icon><PlusOutlined /></template>
        新增作物
      </a-button>
    </div>
    <a-table
      :dataSource="crops"
      :loading="loading"
      rowKey="id"
      :pagination="{ pageSize: 20 }"
      size="small"
    >
      <a-table-column title="名称" dataIndex="name" :width="140" />
      <a-table-column title="类别" dataIndex="category" :width="100" />
      <a-table-column title="学名" dataIndex="scientific_name" :width="200" ellipsis />
      <a-table-column title="描述" dataIndex="description" ellipsis />
      <a-table-column title="操作" :width="160" align="center">
        <template #default="{ record }">
          <a-space>
            <a-button size="small" type="primary" ghost @click="openCropEdit(record)">编辑</a-button>
            <a-button size="small" danger @click="handleDeleteCrop(record.id)">删除</a-button>
          </a-space>
        </template>
      </a-table-column>
    </a-table>

    <!-- Crop modal -->
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
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="学名">
              <a-input v-model:value="cropForm.scientificName" placeholder="如：Oryza sativa" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="类别">
              <a-select v-model:value="cropForm.category" allowClear placeholder="选择类别">
                <a-select-option value="粮食作物">粮食作物</a-select-option>
                <a-select-option value="经济作物">经济作物</a-select-option>
                <a-select-option value="蔬菜">蔬菜</a-select-option>
                <a-select-option value="果树">果树</a-select-option>
                <a-select-option value="花卉">花卉</a-select-option>
                <a-select-option value="其他">其他</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="描述">
          <a-textarea v-model:value="cropForm.description" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { message, Modal } from 'ant-design-vue'
import { listCrops, createCrop, updateCrop, deleteCrop } from '@/apis/crop_manager'

const crops = ref([])
const loading = ref(false)
const cropModalVisible = ref(false)
const cropEditing = ref(null)
const cropForm = ref({})

async function loadCrops() {
  loading.value = true
  try {
    const res = await listCrops()
    crops.value = Array.isArray(res) ? res : res.data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function openCropAdd() {
  cropEditing.value = null
  cropForm.value = { name: '', scientificName: '', category: null, description: '' }
  cropModalVisible.value = true
}

function openCropEdit(item) {
  cropEditing.value = item
  cropForm.value = {
    name: item.name,
    scientificName: item.scientific_name || '',
    category: item.category || null,
    description: item.description || ''
  }
  cropModalVisible.value = true
}

async function saveCrop() {
  try {
    const data = {
      name: cropForm.value.name,
      scientific_name: cropForm.value.scientificName || null,
      category: cropForm.value.category || null,
      description: cropForm.value.description || null
    }
    const res = cropEditing.value
      ? await updateCrop(cropEditing.value.id, data)
      : await createCrop(data)
    message.success(cropEditing.value ? '修改成功' : '添加成功')
    cropModalVisible.value = false
    loadCrops()
  } catch (e) {
    message.error('操作失败: ' + (e.message || ''))
  }
}

function handleDeleteCrop(id) {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除该农作物吗？',
    onOk: async () => {
      try {
        await deleteCrop(id)
        message.success('删除成功')
        loadCrops()
      } catch (e) {
        message.error('删除失败')
      }
    }
  })
}

onMounted(() => {
  loadCrops()
})
</script>

<style lang="less" scoped>
.crop-dict-view {
  padding: 24px;
  height: 100%;
  overflow-y: auto;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
      color: var(--gray-900);
    }
  }
}
</style>
