<template>
  <div class="profile-page">
    <div class="profile-content">
      <!-- 基本信息 -->
      <div class="section-card">
        <h3 class="section-title">基本信息</h3>
        <div class="user-info-row">
          <div class="user-avatar-section">
            <div class="user-avatar">
              <img v-if="userStore.avatar" :src="userStore.avatar" :alt="userStore.username" />
              <div v-else class="avatar-placeholder">{{ userStore.username?.charAt(0)?.toUpperCase() || '?' }}</div>
            </div>
            <a-upload
              :show-upload-list="false"
              :before-upload="beforeUpload"
              @change="handleAvatarChange"
              accept="image/*"
            >
              <a-button size="small" type="primary" ghost :loading="avatarUploading">
                <template #icon><Upload size="14" /></template>
                更换头像
              </a-button>
            </a-upload>
          </div>
          <a-descriptions :column="1" :label-style="{ width: '100px', color: 'var(--gray-700)' }">
            <a-descriptions-item label="用户名">
              <template v-if="!editing">
                {{ userStore.username || '未设置' }}
                <a-button type="link" size="small" @click="startEdit">编辑</a-button>
              </template>
              <template v-else>
                <a-input v-model:value="editForm.username" placeholder="用户名" style="width: 200px" />
              </template>
            </a-descriptions-item>
            <a-descriptions-item label="用户 ID">{{ userStore.userIdLogin || '未设置' }}</a-descriptions-item>
            <a-descriptions-item label="邮箱">
              <template v-if="!editing">
                {{ userStore.email || '未设置' }}
              </template>
              <template v-else>
                <a-input v-model:value="editForm.email" placeholder="邮箱" style="width: 200px" />
              </template>
            </a-descriptions-item>
            <a-descriptions-item label="角色">
              <a-tag :color="roleColor">{{ roleText }}</a-tag>
            </a-descriptions-item>
          </a-descriptions>
          <div v-if="editing" class="edit-actions">
            <a-button type="primary" @click="saveProfile" :loading="saving">保存</a-button>
            <a-button @click="cancelEdit">取消</a-button>
          </div>
        </div>
      </div>

      <!-- 地址与位置 -->
      <div class="section-card">
        <h3 class="section-title">地址与位置</h3>
        <div class="address-row">
          <a-input v-model:value="addressInput" placeholder="请输入详细地址，如：北京市朝阳区望京SOHO" style="flex: 1" allow-clear />
          <a-button type="primary" @click="geocodeAddress" :loading="geocoding">
            <template #icon><Search size="16" /></template>
            定位
          </a-button>
        </div>
        <div v-if="location" class="location-info">
          <span>经度: {{ location.lng.toFixed(6) }}</span>
          <span>纬度: {{ location.lat.toFixed(6) }}</span>
        </div>
        <div ref="mapContainer" class="map-container"></div>
        <div class="address-actions">
          <a-button type="primary" @click="saveAddress" :loading="savingAddress" :disabled="!location">
            <template #icon><Check size="16" /></template>
            保存地址信息
          </a-button>
          <span v-if="savedAddressText" class="saved-hint">已保存: {{ savedAddressText }}</span>
        </div>
      </div>

      <!-- 微信公众号绑定 -->
      <div class="section-card">
        <h3 class="section-title">微信公众号绑定</h3>
        <div v-if="wechatBound" class="bound-info">
          <a-tag color="green">已绑定</a-tag>
          <span v-if="wechatBoundAt" class="bound-time">绑定时间: {{ wechatBoundAt }}</span>
          <a-button type="text" danger size="small" @click="unbindWechat" :loading="unbinding">
            <template #icon><Trash2 size="14" /></template>
            解绑
          </a-button>
        </div>
        <div v-else>
          <p class="binding-desc">
            生成绑定令牌后，将其发送到微信公众号即可完成绑定。令牌永久有效，一次生成后任意时间均可绑定。
          </p>
          <div v-if="wechatToken" class="token-display">
            <div class="token-box">
              <code class="token-text">{{ wechatToken }}</code>
              <a-button size="small" type="link" @click="copyToken">
                <template #icon><Copy size="14" /></template>
              </a-button>
            </div>
            <span class="token-permanent">永久有效</span>
          </div>
          <a-button type="primary" ghost @click="generateToken" :loading="generatingToken">
            <template #icon><Smartphone size="14" /></template>
            生成绑定令牌
          </a-button>
        </div>
      </div>

      <!-- 邮箱绑定 -->
      <div class="section-card">
        <h3 class="section-title">邮箱绑定</h3>
        <div v-if="emailBound" class="bound-info">
          <a-tag color="blue">已绑定</a-tag>
          <span class="bound-time">{{ emailAddress }}</span>
          <a-button type="text" danger size="small" @click="unbindEmailAddress" :loading="emailUnbinding">
            <template #icon><Trash2 size="14" /></template>
            解绑
          </a-button>
        </div>
        <div v-else>
          <p class="binding-desc">绑定邮箱后，系统通知将通过邮件推送到您的邮箱。</p>
          <div class="email-form">
            <a-input v-model:value="emailInput" placeholder="请输入邮箱地址" style="flex: 1" allow-clear />
            <a-button @click="sendEmailCode" :loading="sendingCode" :disabled="!emailInput.trim()">发送验证码</a-button>
          </div>
          <div v-if="codeSent" class="email-form" style="margin-top: 8px">
            <a-input v-model:value="codeInput" placeholder="请输入验证码" style="flex: 1" :max-length="6" />
            <a-button type="primary" @click="verifyEmailCodeFn" :loading="verifyingCode" :disabled="!codeInput.trim()">绑定</a-button>
          </div>
        </div>
      </div>

      <!-- 种植农作物 -->
      <div class="section-card">
        <h3 class="section-title">
          种植农作物
          <a-button type="primary" size="small" @click="showAddCropModal = true" ghost>
            <template #icon><Plus size="14" /></template>
            添加农作物
          </a-button>
        </h3>
        <div v-if="myCrops.length === 0" class="empty-hint">暂未添加农作物</div>
        <div v-else class="crop-list">
          <div v-for="crop in myCrops" :key="crop.id" class="crop-item">
            <div class="crop-info">
              <span class="crop-name">{{ crop.crop_name }}</span>
              <span v-if="crop.nickname" class="crop-nickname">({{ crop.nickname }})</span>
              <span v-if="crop.area" class="crop-area">{{ crop.area }} 亩</span>
              <span v-if="crop.planted_at" class="crop-date">种植于 {{ crop.planted_at }}</span>
            </div>
            <a-button type="text" danger size="small" @click="removeCrop(crop)">
              <template #icon><Trash2 size="14" /></template>
            </a-button>
          </div>
        </div>
      </div>

      <!-- 关注公众号 -->
      <div class="section-card">
        <h3 class="section-title">关注公众号</h3>
        <div class="gzh-qr-wrap">
          <img src="/gzh.jpg" alt="微信公众号" class="gzh-qr-img" />
          <span class="gzh-qr-label">扫码关注微信公众号，获取最新动态</span>
        </div>
      </div>
    </div>

    <!-- 添加农作物弹窗 -->
    <a-modal v-model:open="showAddCropModal" title="添加农作物" :footer="null" width="520px" destroy-on-close>
      <div class="add-crop-form">
        <div class="form-item">
          <label>选择农作物</label>
          <a-select
            v-model:value="newCrop.crop_id"
            style="width: 100%"
            placeholder="请选择要种植的农作物"
            :options="availableCropOptions"
            show-search
            :filter-option="(input, option) => option.label?.toLowerCase().includes(input.toLowerCase())"
          />
        </div>
        <div class="form-item">
          <label>别名/品种（可选）</label>
          <a-input v-model:value="newCrop.nickname" placeholder="如：东北大米" />
        </div>
        <div class="form-row">
          <div class="form-item flex-1">
            <label>种植面积（亩，可选）</label>
            <a-input-number v-model:value="newCrop.area" :min="0" :precision="2" style="width: 100%" placeholder="0.00" />
          </div>
          <div class="form-item flex-1">
            <label>种植日期（可选）</label>
            <a-date-picker v-model:value="newCrop.planted_at" style="width: 100%" placeholder="选择日期" />
          </div>
        </div>
        <div class="form-item">
          <label>备注（可选）</label>
          <a-textarea v-model:value="newCrop.notes" placeholder="备注信息" :rows="2" />
        </div>
        <div class="form-actions">
          <a-button @click="showAddCropModal = false">取消</a-button>
          <a-button type="primary" @click="addCrop" :loading="addingCrop" :disabled="!newCrop.crop_id">添加</a-button>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import { listCrops, listMyCrops, addMyCrop, removeMyCrop, updateAddress } from '@/apis/crop_manager'
import { generateWeChatBindingToken, getWeChatBindingStatus, unbindWeChat } from '@/apis/wechat_api'
import { sendEmailCode as sendEmailCodeApi, verifyEmailCode as verifyEmailCodeApi, getEmailBindingStatus, unbindEmail } from '@/apis/email_api'
import { Upload, Search, Check, Plus, Trash2, Smartphone, Copy } from 'lucide-vue-next'
import dayjs from 'dayjs'

const userStore = useUserStore()

// ---- 基本信息 ----
const editing = ref(false)
const saving = ref(false)
const avatarUploading = ref(false)
const editForm = reactive({ username: '', email: '' })

const roleText = computed(() => {
  if (userStore.isSuperAdmin) return '超级管理员'
  if (userStore.isAdmin) return '管理员'
  return '普通用户'
})
const roleColor = computed(() => {
  if (userStore.isSuperAdmin) return 'red'
  if (userStore.isAdmin) return 'blue'
  return 'green'
})

const startEdit = () => {
  editForm.username = userStore.username || ''
  editForm.email = userStore.email || ''
  editing.value = true
}
const cancelEdit = () => { editing.value = false }
const saveProfile = async () => {
  saving.value = true
  try {
    await userStore.updateProfile({
      username: editForm.username?.trim() || undefined,
      email: editForm.email || undefined
    })
    message.success('保存成功')
    editing.value = false
  } catch (e) {
    message.error(e.message || '保存失败')
  } finally {
    saving.value = false
  }
}

const beforeUpload = (file) => {
  if (!file.type.startsWith('image/')) { message.error('只能上传图片'); return false }
  if (file.size > 5 * 1024 * 1024) { message.error('图片不能超过 5MB'); return false }
  return true
}
const handleAvatarChange = async (info) => {
  if (info.file.status === 'uploading') { avatarUploading.value = true; return }
  if (info.file.originFileObj || info.file) {
    avatarUploading.value = true
    try {
      await userStore.uploadAvatar(info.file.originFileObj || info.file)
      message.success('头像已更新')
    } catch (e) {
      message.error('头像上传失败')
    } finally {
      avatarUploading.value = false
    }
  }
}

// ---- 高德地图加载 (v1.4.15，无需 securityJsCode/服务域名白名单) ----
const AMAP_KEY = import.meta.env.VITE_AMAP_KEY || '42123fd3f21408fc4c2b9c9443ad38ca'
const AMAP_SECURITY_JS_CODE = import.meta.env.VITE_AMAP_SECURITY_JS_CODE || 'f80aa563310d7854f8676e8340fb3848'
const amapReady = ref(false)
const amapLoading = ref(false)
let amapPromise = null

function loadAMap() {
  if (amapPromise) return amapPromise
  if (window.AMap) {
    amapReady.value = true
    amapPromise = Promise.resolve(window.AMap)
    return amapPromise
  }
  amapPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.onload = () => {
      // v1.4 脚本加载完成后 AMap 应该立即可用
      if (window.AMap) {
        console.log('AMap v1.4.15 loaded successfully')
        resolve(window.AMap)
        return
      }
      const check = setInterval(() => {
        if (window.AMap) { clearInterval(check); resolve(window.AMap) }
      }, 200)
      setTimeout(() => { clearInterval(check); reject(new Error('高德地图初始化超时')) }, 15000)
    }
    script.onerror = () => { amapPromise = null; reject(new Error('高德地图脚本加载失败')) }
    script.src = `https://webapi.amap.com/maps?v=1.4.15&key=${AMAP_KEY}`
    document.head.appendChild(script)
  })
  return amapPromise
}

async function ensureAMap() {
  if (window.AMap && amapReady.value) return
  amapLoading.value = true
  try {
    await loadAMap()
    amapReady.value = true
  } catch (e) {
    message.error(e.message)
    throw e
  } finally {
    amapLoading.value = false
  }
}

// ---- 地址与地图 ----
const addressInput = ref(userStore.address || '')
const geocoding = ref(false)
const savingAddress = ref(false)
const savedAddressText = ref(userStore.address || '')
const location = ref(userStore.latitude && userStore.longitude
  ? { lat: Number(userStore.latitude), lng: Number(userStore.longitude) }
  : null)
const mapContainer = ref(null)
let mapInstance = null
let markerInstance = null

async function initMap() {
  if (!mapContainer.value || mapInstance) return
  await ensureAMap()
  const defaultLoc = location.value || { lat: 39.9042, lng: 116.4074 }
  try {
    mapInstance = new AMap.Map(mapContainer.value, {
      zoom: 13,
      center: [defaultLoc.lng, defaultLoc.lat]
    })
    // 确保地图在容器渲染完成后正确显示
    setTimeout(() => { mapInstance?.resize?.() }, 100)
    markerInstance = new AMap.Marker({
      position: [defaultLoc.lng, defaultLoc.lat],
      draggable: true
    })
    mapInstance.add(markerInstance)
    markerInstance.on('dragend', (e) => {
      const pos = e.target.getPosition()
      location.value = { lat: pos.getLat(), lng: pos.getLng() }
    })
  } catch (e) {
    console.error('地图初始化失败:', e)
    message.error('地图初始化失败')
  }
}

function updateMarker(lat, lng) {
  if (!mapInstance) return
  const pos = [lng, lat]
  if (markerInstance) markerInstance.setPosition(pos)
  else {
    markerInstance = new AMap.Marker({ position: pos, draggable: true })
    mapInstance.add(markerInstance)
    markerInstance.on('dragend', (e) => {
      const p = e.target.getPosition()
      location.value = { lat: p.getLat(), lng: p.getLng() }
    })
  }
  mapInstance.setCenter(pos)
}

// 直接调用高德 REST API 进行地理编码，避免 JS SDK 的 JSONP 回调问题
async function geocodeAddress() {
  if (!addressInput.value?.trim()) {
    message.warning('请输入地址')
    return
  }
  geocoding.value = true
  try {
    const resp = await fetch(
      `https://restapi.amap.com/v3/geocode/geo?key=${AMAP_KEY}&address=${encodeURIComponent(addressInput.value.trim())}&output=json`
    )
    const data = await resp.json()
    if (data.status === '1' && data.geocodes?.length > 0) {
      const [lng, lat] = data.geocodes[0].location.split(',').map(Number)
      location.value = { lat, lng }
      await nextTick()
      initMap()
      updateMarker(lat, lng)
      message.success('定位成功')
    } else {
      message.warning('未找到该地址，请尝试更详细的地址')
    }
  } catch (e) {
    message.error('地理编码请求失败: ' + (e.message || ''))
  } finally {
    geocoding.value = false
  }
}

const saveAddress = async () => {
  if (!location.value) return
  savingAddress.value = true
  try {
    const res = await updateAddress({
      address: addressInput.value,
      latitude: location.value.lat,
      longitude: location.value.lng
    })
    savedAddressText.value = addressInput.value
    // 同步本地 store
    userStore.address = addressInput.value
    userStore.latitude = location.value.lat
    userStore.longitude = location.value.lng
    message.success('地址信息已保存')
  } catch (e) {
    message.error(e.message || '保存地址失败')
  } finally {
    savingAddress.value = false
  }
}

// ---- 种植农作物 ----
const myCrops = ref([])
const allCrops = ref([])
const showAddCropModal = ref(false)
const addingCrop = ref(false)
const newCrop = reactive({ crop_id: undefined, nickname: '', area: null, planted_at: null, notes: '' })

const availableCropOptions = computed(() => {
  const myCropIds = new Set(myCrops.value.map(c => c.crop_id))
  return allCropOptions.value.filter(c => !myCropIds.has(c.value))
})
const allCropOptions = computed(() =>
  allCrops.value.map(c => ({ label: c.name, value: c.id }))
)

const loadMyCrops = async () => {
  try {
    const res = await listMyCrops()
    myCrops.value = (res.data || res || []).map(c => ({
      ...c,
      key: c.id
    }))
  } catch (e) {
    console.error('加载农作物失败', e)
  }
}

const loadAllCrops = async () => {
  try {
    const res = await listCrops()
    allCrops.value = res.data || res || []
  } catch (e) {
    console.error('加载农作物字典失败', e)
  }
}

const addCrop = async () => {
  if (!newCrop.crop_id) return
  addingCrop.value = true
  try {
    const payload = { crop_id: newCrop.crop_id }
    if (newCrop.nickname) payload.nickname = newCrop.nickname
    if (newCrop.area !== null && newCrop.area !== undefined) payload.area = newCrop.area
    if (newCrop.planted_at) payload.planted_at = dayjs(newCrop.planted_at).format('YYYY-MM-DD')
    if (newCrop.notes) payload.notes = newCrop.notes
    await addMyCrop(payload)
    message.success('添加成功')
    showAddCropModal.value = false
    Object.assign(newCrop, { crop_id: undefined, nickname: '', area: null, planted_at: null, notes: '' })
    await loadMyCrops()
  } catch (e) {
    message.error(e.message || '添加失败')
  } finally {
    addingCrop.value = false
  }
}

const removeCrop = async (crop) => {
  try {
    await removeMyCrop(crop.id)
    message.success('已移除')
    await loadMyCrops()
  } catch (e) {
    message.error(e.message || '移除失败')
  }
}

// ---- 微信公众号绑定 ----
const wechatBound = ref(false)
const wechatBoundAt = ref('')
const wechatToken = ref('')
const generatingToken = ref(false)
const unbinding = ref(false)
const tokenExpiresAt = ref(0)

const generateToken = async () => {
  generatingToken.value = true
  try {
    const res = await generateWeChatBindingToken()
    wechatToken.value = res.data.token
    tokenExpiresAt.value = Date.now() + res.data.expires_in_minutes * 60 * 1000
  } catch (e) {
    message.error(e.message || '生成令牌失败')
  } finally {
    generatingToken.value = false
  }
}

const copyToken = async () => {
  try {
    await navigator.clipboard.writeText(wechatToken.value)
    message.success('令牌已复制到剪贴板')
  } catch {
    // fallback: 创建临时 textarea
    const ta = document.createElement('textarea')
    ta.value = wechatToken.value
    ta.style.position = 'fixed'
    ta.style.opacity = '0'
    document.body.appendChild(ta)
    ta.select()
    try {
      document.execCommand('copy')
      message.success('令牌已复制到剪贴板')
    } catch {
      message.error('复制失败，请手动复制')
    }
    document.body.removeChild(ta)
  }
}

const loadBindingStatus = async () => {
  try {
    const res = await getWeChatBindingStatus()
    wechatBound.value = res.data.is_bound
    wechatBoundAt.value = res.data.bound_at || ''
  } catch (e) {
    // 微信服务未配置时静默失败
    if (e.response?.status !== 503) {
      console.error('加载微信绑定状态失败', e)
    }
  }
}

const unbindWechat = async () => {
  unbinding.value = true
  try {
    await unbindWeChat()
    message.success('已解绑')
    wechatBound.value = false
    wechatBoundAt.value = ''
  } catch (e) {
    message.error(e.message || '解绑失败')
  } finally {
    unbinding.value = false
  }
}


// ---- 邮箱绑定 ----
const emailBound = ref(false)
const emailAddress = ref('')
const emailInput = ref('')
const codeInput = ref('')
const codeSent = ref(false)
const sendingCode = ref(false)
const verifyingCode = ref(false)
const emailUnbinding = ref(false)

const sendEmailCode = async () => {
  const email = emailInput.value.trim()
  if (!email) return
  sendingCode.value = true
  try {
    await sendEmailCodeApi(email)
    message.success('验证码已发送')
    codeSent.value = true
  } catch (e) {
    message.error(e.message || '发送验证码失败')
  } finally {
    sendingCode.value = false
  }
}

const verifyEmailCodeFn = async () => {
  const email = emailInput.value.trim()
  const code = codeInput.value.trim()
  if (!email || !code) return
  verifyingCode.value = true
  try {
    await verifyEmailCodeApi(email, code)
    message.success('邮箱绑定成功')
    emailBound.value = true
    emailAddress.value = email
    codeSent.value = false
    emailInput.value = ''
    codeInput.value = ''
  } catch (e) {
    message.error(e.message || '绑定失败')
  } finally {
    verifyingCode.value = false
  }
}

const unbindEmailAddress = async () => {
  emailUnbinding.value = true
  try {
    await unbindEmail()
    message.success('邮箱已解绑')
    emailBound.value = false
    emailAddress.value = ''
  } catch (e) {
    message.error(e.message || '解绑失败')
  } finally {
    emailUnbinding.value = false
  }
}

const loadEmailBindingStatus = async () => {
  try {
    const res = await getEmailBindingStatus()
    emailBound.value = res.data.is_bound
    if (res.data.full_email) {
      emailAddress.value = res.data.full_email
    }
  } catch (e) {
    if (e.response?.status !== 503) {
      console.error('加载邮箱绑定状态失败', e)
    }
  }
}


onMounted(async () => {
  await Promise.all([loadMyCrops(), loadAllCrops(), loadBindingStatus(), loadEmailBindingStatus()])
  await nextTick()
  try {
    await ensureAMap()
    await nextTick()
    initMap()
  } catch (e) {
    console.error('地图初始化失败:', e)
    message.error('地图加载失败')
  }
})

</script>

<style lang="less" scoped>
.profile-page {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
  background: var(--gray-50);
}

.profile-content {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  background: var(--gray-0);
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  padding: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-1000);
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gzh-qr-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 12px 0;
}

.gzh-qr-img {
  width: 120px;
  height: 120px;
  border-radius: 8px;
}

.gzh-qr-label {
  font-size: 0.85rem;
  color: var(--gray-500);
}

.user-info-row {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.user-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;

  .user-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    overflow: hidden;
    background: var(--gray-100);

    img { width: 100%; height: 100%; object-fit: cover; }
    .avatar-placeholder {
      width: 100%; height: 100%;
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; font-weight: 600; color: var(--gray-500);
    }
  }
}

.edit-actions {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.address-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.location-info {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: var(--gray-600);
  margin-bottom: 8px;
}

.map-container {
  width: 100%;
  height: 280px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-200);
  z-index: 1;
}

.address-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 12px;
}

.saved-hint {
  font-size: 13px;
  color: var(--color-success-600);
}

.crop-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.crop-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--gray-50);
  border-radius: 8px;
  border: 1px solid var(--gray-150);

  .crop-info {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .crop-name { font-weight: 600; color: var(--gray-1000); }
  .crop-nickname { color: var(--gray-600); font-size: 13px; }
  .crop-area { color: var(--main-color); font-size: 13px; }
  .crop-date { color: var(--gray-500); font-size: 12px; }
}

.empty-hint {
  text-align: center;
  padding: 24px;
  color: var(--gray-500);
}

.binding-desc {
  color: var(--gray-600);
  font-size: 13px;
  margin: 0 0 16px 0;
  line-height: 1.6;
}

.token-display {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.token-box {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 8px 12px;
}

.token-text {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  color: var(--main-color);
  font-family: 'Courier New', monospace;
  user-select: all;
  -webkit-user-select: all;
}

.token-expiry {
  font-size: 12px;
  color: var(--color-warning-600);
}

.token-permanent {
  font-size: 12px;
  color: var(--color-success-600);
}

.bound-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bound-time {
  font-size: 13px;
  color: var(--gray-600);
}


.email-form {
  display: flex;
  gap: 8px;
  align-items: center;
}

.add-crop-form {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .form-item {
    label {
      display: block;
      font-size: 13px;
      color: var(--gray-700);
      margin-bottom: 4px;
      font-weight: 500;
    }
  }

  .form-row {
    display: flex;
    gap: 12px;
  }

  .flex-1 { flex: 1; }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 8px;
  }
}
</style>
