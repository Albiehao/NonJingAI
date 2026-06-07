<template>
  <div class="webhook-admin">
    <div class="page-header">
      <h2>Webhook 推送管理</h2>
      <a-space>
        <a-button @click="openQuickPushModal">
          <template #icon><SendOutlined /></template>
          快速推送
        </a-button>
        <a-button type="primary" @click="openCreateModal">
          <template #icon><PlusOutlined /></template>
          新增推送源
        </a-button>
      </a-space>
    </div>

    <!-- 使用说明 -->
    <a-card class="usage-card">
      <div class="usage-title">
        <InfoCircleOutlined /> 如何使用
      </div>
      <div class="usage-steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-body">
            <div class="step-title">新建推送源</div>
            <div class="step-desc">点击右上角「新增推送源」按钮，填写名称和推送消息模板后保存</div>
          </div>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-body">
            <div class="step-title">获取 Webhook URL</div>
            <div class="step-desc">创建成功后，在下方的列表中复制对应推送源的 Webhook URL，格式为：</div>
            <div class="step-code"><code>POST {{ WEBHOOK_BASE_URL }}/{token}</code></div>
            <div class="step-desc">其中 <code>{token}</code> 是系统自动生成的密钥令牌，每个推送源唯一</div>
          </div>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-body">
            <div class="step-title">外部服务调用</div>
            <div class="step-desc">向 Webhook URL 发送 POST 请求即可触发推送，请求体格式如下：</div>
            <div class="step-code">
<pre>POST {{ WEBHOOK_BASE_URL }}/{token}
Content-Type: application/json

{
  "message": "今晚有暴雨，请注意防范",
  "filters": {
    "crops": ["水稻", "小麦"],
    "geo": { "lat": 30.5, "lng": 114.3 },
    "geo_radius_km": 10
  }
}</pre>
            </div>
          </div>
        </div>
      </div>
      <a-collapse ghost style="margin-top: 8px">
        <a-collapse-panel key="fields" header="请求体字段说明">
          <a-table :data-source="fieldDocs" :columns="fieldColumns" :pagination="false" size="small" row-key="field" />
        </a-collapse-panel>
      </a-collapse>
    </a-card>

    <!-- Webhook 源列表 -->
    <a-card title="推送源管理" style="margin-top: 16px">
      <a-table
        :data-source="sources"
        :columns="columns"
        :pagination="{ pageSize: 10 }"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'is_active'">
            <a-switch
              :checked="record.is_active"
              @change="(checked) => toggleActive(record, checked)"
              size="small"
            />
          </template>
          <template v-if="column.key === 'webhook_url'">
            <div class="url-cell">
              <a-typography-text copyable :content="getWebhookUrl(record.secret_token)" style="font-size: 12px; word-break: break-all;">
                {{ getWebhookUrl(record.secret_token) }}
              </a-typography-text>
            </div>
          </template>
          <template v-if="column.key === 'actions'">
            <a-space>
              <a-button size="small" @click="openTestModal(record)">测试</a-button>
              <a-button size="small" @click="openEditModal(record)">编辑</a-button>
              <a-button size="small" danger @click="handleDelete(record)">删除</a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- Webhook 事件日志 -->
    <a-card title="推送事件日志" style="margin-top: 16px">
      <a-table
        :data-source="events"
        :columns="eventColumns"
        :pagination="{ pageSize: 5 }"
        row-key="id"
        size="small"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="statusColor(record.status)">{{ statusLabel(record.status) }}</a-tag>
          </template>
          <template v-if="column.key === 'created_at'">
            {{ formatTime(record.created_at) }}
          </template>
          <template v-if="column.key === 'raw_body'">
            <a-button size="small" type="link" @click="viewRawBody(record)">查看</a-button>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 创建/编辑弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="editingSource ? '编辑推送源' : '新建推送源'"
      :confirm-loading="submitting"
      @ok="handleSubmit"
      @cancel="modalVisible = false"
      width="640px"
      :destroy-on-close="true"
    >
      <a-form layout="vertical" :model="form" ref="formRef">
        <a-form-item label="名称" name="name" :rules="[{ required: true, message: '请输入名称' }]">
          <a-input v-model:value="form.name" placeholder="例如：天气预警推送" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea v-model:value="form.description" :rows="2" placeholder="可选描述" />
        </a-form-item>
        <a-alert
          message="系统将自动使用「推送消息助手」智能体处理推送"
          type="info"
          show-icon
          style="margin-bottom: 16px"
        />
        <a-form-item
          label="提示词模板"
          name="prompt_template"
          :rules="[{ required: true, message: '请输入提示词模板' }]"
          extra="推送消息内容，用户信息（姓名、手机号、地址、农作物）由系统自动注入"
        >
          <a-textarea
            v-model:value="form.prompt_template"
            :rows="3"
            placeholder="例如：您有一则新的气象预警消息"
          />
        </a-form-item>
        <a-form-item
          label="额外提示词（可选）"
          name="extra_prompt"
          extra="附加到推送消息助手的基础提示词之后，自定义语气或行为"
        >
          <a-textarea
            v-model:value="form.extra_prompt"
            :rows="2"
            placeholder="例如：语气要正式、紧迫一些"
          />
        </a-form-item>
        <a-form-item label="状态" name="is_active">
          <a-switch v-model:checked="form.is_active" checked-children="启用" un-checked-children="停用" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 测试弹窗 -->
    <a-modal
      v-model:open="testModalVisible"
      title="测试推送源"
      :footer="null"
      width="700px"
      :destroy-on-close="true"
    >
      <a-form layout="vertical">
        <a-form-item
          label="模拟推送数据 (JSON)"
          extra="测试消息和筛选条件的渲染效果"
        >
          <a-textarea
            v-model:value="testMockBody"
            :rows="4"
            placeholder='{"message": "今晚有暴雨", "filters": {"crops": ["水稻"], "geo": {"lat": 30.5, "lng": 114.3}}}'
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" :loading="testing" @click="runTest">测试预览</a-button>
        </a-form-item>
      </a-form>
      <a-divider />
      <a-form layout="vertical">
        <a-form-item label="发送给用户的内容预览">
          <a-textarea
            v-model:value="testPreview"
            :rows="4"
            readonly
            placeholder="点击测试按钮查看渲染结果"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 原始数据查看弹窗 -->
    <a-modal
      v-model:open="rawBodyVisible"
      title="Webhook 原始数据"
      :footer="null"
      width="700px"
    >
      <pre style="max-height: 400px; overflow: auto; background: #f5f5f5; padding: 12px; border-radius: 4px; white-space: pre-wrap; word-break: break-all;">{{ viewingRawBody }}</pre>
    </a-modal>

    <!-- 快速推送弹窗 -->
    <a-modal
      v-model:open="quickPushVisible"
      title="快速推送"
      :confirm-loading="quickPushing"
      @ok="handleQuickPush"
      @cancel="quickPushVisible = false"
      width="640px"
      :destroy-on-close="true"
    >
      <a-form layout="vertical">
        <a-form-item
          label="推送源"
          name="source_id"
          extra="不选择则自动使用第一个启用的推送源"
        >
          <a-select v-model:value="quickPushForm.source_id" allow-clear placeholder="自动选择" style="width: 100%">
            <a-select-option v-for="s in sources" :key="s.id" :value="s.id">
              {{ s.name }}{{ s.is_active ? '' : ' (已停用)' }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
          label="推送消息"
          name="message"
          :rules="[{ required: true, message: '请输入推送消息' }]"
        >
          <a-textarea
            v-model:value="quickPushForm.message"
            :rows="3"
            placeholder="例如：今晚有暴雨，请注意防范"
          />
        </a-form-item>
        <a-divider>筛选条件（可选）</a-divider>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="农作物筛选" name="crops">
              <a-select
                v-model:value="quickPushForm.crops"
                mode="tags"
                placeholder="输入农作物名称"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="地址包含" name="address_contains">
              <a-input v-model:value="quickPushForm.address_contains" placeholder="例如：江汉区" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="纬度" name="lat">
              <a-input-number v-model:value="quickPushForm.lat" style="width: 100%" placeholder="30.5" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="经度" name="lng">
              <a-input-number v-model:value="quickPushForm.lng" style="width: 100%" placeholder="114.3" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="筛选半径(km)" name="geo_radius_km">
              <a-input-number v-model:value="quickPushForm.geo_radius_km" :min="1" style="width: 100%" placeholder="10" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
      <a-alert v-if="quickPushResult" :message="quickPushResult" type="success" show-icon />
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { PlusOutlined, InfoCircleOutlined, SendOutlined } from '@ant-design/icons-vue'
import { webhookApi } from '@/apis/webhook_api'
import { message } from 'ant-design-vue'

const WEBHOOK_BASE_URL = `${window.location.origin}/api/webhook/receive`

const loading = ref(false)
const submitting = ref(false)
const sources = ref([])
const events = ref([])
const modalVisible = ref(false)
const editingSource = ref(null)
const formRef = ref(null)
const form = ref({
  name: '',
  description: '',
  prompt_template: '',
  extra_prompt: '',
  is_active: true,
})

const testModalVisible = ref(false)
const testing = ref(false)
const testSource = ref(null)
const testMockBody = ref('{\n  "message": "这是一条测试消息",\n  "type": "info"\n}')
const testPreview = ref('')

const rawBodyVisible = ref(false)
const viewingRawBody = ref('')

const quickPushVisible = ref(false)
const quickPushing = ref(false)
const quickPushResult = ref('')
const quickPushForm = ref({
  source_id: undefined,
  message: '',
  crops: [],
  address_contains: '',
  lat: undefined,
  lng: undefined,
  geo_radius_km: 10,
})

const openQuickPushModal = () => {
  quickPushForm.value = {
    source_id: undefined,
    message: '',
    crops: [],
    address_contains: '',
    lat: undefined,
    lng: undefined,
    geo_radius_km: 10,
  }
  quickPushResult.value = ''
  quickPushVisible.value = true
}

const handleQuickPush = async () => {
  if (!quickPushForm.value.message) {
    message.warning('请输入推送消息')
    return
  }
  quickPushing.value = true
  quickPushResult.value = ''
  try {
    const data = { message: quickPushForm.value.message }
    if (quickPushForm.value.source_id) data.source_id = quickPushForm.value.source_id
    if (quickPushForm.value.crops && quickPushForm.value.crops.length) data.crops = quickPushForm.value.crops
    if (quickPushForm.value.address_contains) data.address_contains = quickPushForm.value.address_contains
    if (quickPushForm.value.lat != null) data.lat = quickPushForm.value.lat
    if (quickPushForm.value.lng != null) data.lng = quickPushForm.value.lng
    if (quickPushForm.value.geo_radius_km != null) data.geo_radius_km = quickPushForm.value.geo_radius_km

    const res = await webhookApi.quickPush(data)
    message.success(res.message || '推送任务已提交')
    quickPushVisible.value = false
    await loadData()
  } catch (e) {
    console.error('快速推送失败:', e)
    message.error('推送失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    quickPushing.value = false
  }
}

const fieldColumns = [
  { title: '字段', dataIndex: 'field', key: 'field', width: 180 },
  { title: '类型', dataIndex: 'type', key: 'type', width: 100 },
  { title: '必填', dataIndex: 'required', key: 'required', width: 60 },
  { title: '说明', dataIndex: 'desc', key: 'desc' },
]

const fieldDocs = [
  { field: 'message', type: 'string', required: '否', desc: '推送消息内容，合并到提示词模板后发送给用户' },
  { field: 'filters.crops', type: 'string[]', required: '否', desc: '按种植农作物名称筛选用户，如 ["水稻", "小麦"]' },
  { field: 'filters.geo', type: 'object', required: '否', desc: '按经纬度筛选，格式：{"lat": 30.5, "lng": 114.3}' },
  { field: 'filters.geo_radius_km', type: 'number', required: '否', desc: '经纬度筛选半径，默认 10 公里' },
  { field: 'filters.address_contains', type: 'string', required: '否', desc: '按地址模糊匹配' },
  { field: 'user_ids', type: 'string[]', required: '否', desc: '指定用户 ID 列表' },
  { field: 'title', type: 'string', required: '否', desc: '消息标题，与 message 二选一' },
]

const columns = [
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', key: 'is_active', width: 70 },
  { title: 'Webhook URL', key: 'webhook_url' },
  { title: '操作', key: 'actions', width: 200 },
]

const eventColumns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
  { title: '源', dataIndex: 'source_id', key: 'source_id', width: 60 },
  { title: '状态', key: 'status', width: 80 },
  { title: '错误信息', dataIndex: 'error_message', key: 'error_message', ellipsis: true },
  { title: '时间', key: 'created_at', width: 170 },
]

const getWebhookUrl = (token) => `${WEBHOOK_BASE_URL}/${token}`

const statusColor = (status) => {
  const map = { pending: 'orange', processing: 'blue', completed: 'green', failed: 'red' }
  return map[status] || 'default'
}

const statusLabel = (status) => {
  const map = { pending: '待处理', processing: '处理中', completed: '已完成', failed: '失败' }
  return map[status] || status
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 19) : '-'

const loadData = async () => {
  loading.value = true
  try {
    const [sourceRes, eventRes] = await Promise.all([
      webhookApi.listSources(),
      webhookApi.listEvents(),
    ])
    sources.value = sourceRes.data || []
    events.value = eventRes.data || []
  } catch (e) {
    console.error('加载数据失败:', e)
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingSource.value = null
  form.value = { name: '', description: '', prompt_template: '', extra_prompt: '', is_active: true }
  modalVisible.value = true
}

const openEditModal = (record) => {
  editingSource.value = record
  form.value = {
    name: record.name,
    description: record.description || '',
    prompt_template: record.prompt_template,
    extra_prompt: record.extra_prompt || '',
    is_active: record.is_active,
  }
  modalVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitting.value = true
  try {
    if (editingSource.value) {
      await webhookApi.updateSource(editingSource.value.id, form.value)
      message.success('更新成功')
    } else {
      const res = await webhookApi.createSource({
        ...form.value,
        agent_id: 'WebhookAgent',
      })
      message.success('创建成功，请在列表中复制 Webhook URL')
    }
    modalVisible.value = false
    await loadData()
  } catch (e) {
    console.error('提交失败:', e)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (record) => {
  try {
    await webhookApi.deleteSource(record.id)
    message.success('删除成功')
    await loadData()
  } catch (e) {
    console.error('删除失败:', e)
  }
}

const toggleActive = async (record, checked) => {
  try {
    await webhookApi.updateSource(record.id, { is_active: checked })
    await loadData()
  } catch (e) {
    console.error('更新状态失败:', e)
  }
}

const openTestModal = (record) => {
  testSource.value = record
  testMockBody.value = '{\n  "message": "这是一条测试消息",\n  "type": "info"\n}'
  testPreview.value = ''
  testModalVisible.value = true
}

const runTest = async () => {
  testing.value = true
  try {
    const res = await webhookApi.testSource(testSource.value.id, testMockBody.value)
    testPreview.value = res.data?.preview || '(无输出)'
  } catch (e) {
    console.error('测试失败:', e)
  } finally {
    testing.value = false
  }
}

const viewRawBody = (record) => {
  viewingRawBody.value = record.raw_body || '(空)'
  rawBodyVisible.value = true
}

onMounted(() => {
  loadData()
})
</script>

<style lang="less" scoped>
.webhook-admin {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
      color: var(--gray-1000);
    }
  }

  .url-cell {
    max-width: 400px;
    overflow: hidden;
  }

  :deep(.ant-alert) {
    border-radius: 6px;
  }

  .usage-card {
    background: var(--gray-25);
    border: 1px solid var(--gray-200);

    .usage-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--gray-1000);
      margin-bottom: 16px;
    }
  }

  .usage-steps {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .step {
    display: flex;
    gap: 12px;

    .step-number {
      flex-shrink: 0;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--main-color);
      color: #fff;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .step-body {
      flex: 1;
      min-width: 0;
    }

    .step-title {
      font-weight: 600;
      font-size: 14px;
      color: var(--gray-1000);
      margin-bottom: 4px;
    }

    .step-desc {
      font-size: 13px;
      color: var(--gray-700);
      margin-bottom: 4px;
      line-height: 1.6;
    }

    .step-code {
      margin: 6px 0;

      pre {
        background: var(--gray-100);
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 13px;
        overflow-x: auto;
        margin: 0;
        line-height: 1.5;
      }
    }
  }

  .url-cell {
    max-width: 350px;
    overflow: hidden;
  }
}
</style>
