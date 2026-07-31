<template>
  <div class="user-center" :class="{ 'light-mode': isLightMode }">
    <main class="user-main">
      <!-- 用户信息卡片 -->
      <section class="user-profile">
        <div class="profile-header">
          <h2 class="profile-title">用户中心</h2>
        </div>

        <div class="profile-card">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img
                v-if="userAvatar"
                :src="avatarFullUrl"
                :alt="username"
                class="avatar-img"
              />
              <div v-else class="avatar-placeholder">
                <span class="avatar-text">{{ avatarText }}</span>
              </div>
            </div>
            <label class="avatar-upload-btn">
              <input
                type="file"
                accept="image/*"
                hidden
                @change="handleAvatarChange"
              />
              <span>更换头像</span>
            </label>
          </div>

          <div class="profile-info">
            <div class="info-row">
              <span class="info-label">用户名</span>
              <div class="info-value-wrapper">
                <input
                  v-if="editing"
                  v-model="editForm.username"
                  type="text"
                  class="info-input"
                  placeholder="请输入用户名"
                />
                <span v-else class="info-value">{{ userInfo.username || '-' }}</span>
              </div>
            </div>
            <div class="info-row">
              <span class="info-label">手机号</span>
              <div class="info-value-wrapper">
                <input
                  v-if="editing"
                  v-model="editForm.phoneNumber"
                  type="text"
                  class="info-input"
                  placeholder="请输入手机号"
                />
                <span v-else class="info-value">{{ userInfo.phoneNumber || '未设置' }}</span>
              </div>
            </div>
            <div class="info-row">
              <span class="info-label">角色</span>
              <span class="info-value role-badge">{{ roleText }}</span>
            </div>
          </div>

          <div class="profile-actions">
            <button v-if="!editing" type="button" class="action-btn" @click="startEdit">
              编辑信息
            </button>
            <template v-else>
              <button type="button" class="action-btn primary" @click="saveEdit">
                保存
              </button>
              <button type="button" class="action-btn" @click="cancelEdit">
                取消
              </button>
            </template>
          </div>
        </div>
      </section>

      <!-- 用户作物关联 -->
      <section class="user-crops">
        <div class="crops-header">
          <h3 class="crops-title">我的作物</h3>
          <button type="button" class="add-btn" @click="openAddCropModal">添加作物</button>
        </div>

        <div v-if="loadingCrops" class="crops-loading">加载中...</div>
        <div v-else-if="userCrops.length === 0" class="crops-empty">
          <p>暂无关联作物，点击上方按钮添加</p>
        </div>
        <div v-else class="crops-grid">
          <div v-for="item in userCrops" :key="item.associationId" class="crop-card">
            <div class="crop-header">
              <span class="crop-name">{{ item.cropName || `作物(${item.cropId})` }}</span>
              <button type="button" class="crop-remove-btn" @click="removeCrop(item.associationId)">移除</button>
            </div>
            <p class="crop-desc">{{ item.scientificName || '-' }}</p>
            <p class="crop-time">关联时间: {{ item.updatedAt || '-' }}</p>
          </div>
        </div>
      </section>

      <!-- 添加作物弹窗 -->
      <div v-if="addCropModalOpen" class="modal-mask" @click.self="closeAddCropModal">
        <div class="modal-content">
          <h4 class="modal-title">添加作物关联</h4>
          <div class="modal-field">
            <label class="modal-label">选择作物</label>
            <div class="pseudo-select">
              <button type="button" class="select-trigger" @click="cropMenuOpen = !cropMenuOpen">
                {{ selectedCropName }}
              </button>
              <ul v-if="cropMenuOpen" class="select-menu">
                <li v-for="c in crops" :key="c.id" @click="selectCrop(c.id)">{{ c.name }}</li>
              </ul>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" class="modal-btn primary" @click="confirmAddCrop">确认添加</button>
            <button type="button" class="modal-btn" @click="closeAddCropModal">取消</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { API_BASE_URL } from '@/config'
import { getUserById, updateUser } from '@/api/user'
import { getUserCropsByUserId, addUserCrop, deleteUserCrop } from '@/api/userCrops'
import { getAllCrops } from '@/api/crops'

export default {
  name: 'UserCenter',
  props: {
    isLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      userId: null,
      username: '',
      userAvatar: '',
      userInfo: {},
      editing: false,
      editForm: {
        username: '',
        phoneNumber: ''
      },
      avatarFile: null,
      userCrops: [],
      crops: [],
      loadingCrops: false,
      addCropModalOpen: false,
      cropMenuOpen: false,
      selectedCropId: null
    }
  },
  computed: {
    avatarText() {
      return this.username ? this.username.slice(0, 1).toUpperCase() : 'U'
    },
    avatarFullUrl() {
      if (!this.userAvatar) return ''
      // base64格式直接返回（用于预览）
      if (this.userAvatar.startsWith('data:')) return this.userAvatar
      // 完整URL直接返回（绝对路径转为相对路径，兼容已存域名的情况）
      if (this.userAvatar.startsWith('http')) {
        try { return new URL(this.userAvatar).pathname } catch { return this.userAvatar }
      }
      // 相对路径拼接后端地址
      return API_BASE_URL + this.userAvatar
    },
    roleText() {
      const role = localStorage.getItem('role') || ''
      if (role === 'ADMIN') return '管理员'
      return '普通用户'
    },
    selectedCropName() {
      if (!this.selectedCropId) return '请选择作物'
      const crop = this.crops.find(c => c.id === this.selectedCropId)
      return crop ? crop.name : '请选择作物'
    }
  },
  created() {
    this.initUser()
  },
  mounted() {
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleOutsideClick)
  },
  methods: {
    async initUser() {
      this.userId = parseInt(localStorage.getItem('userId') || '0')
      this.username = localStorage.getItem('username') || ''
      // 先从后端获取用户信息（包括头像）
      await this.loadUserInfo()
      // 如果后端有头像，更新localStorage
      if (this.userInfo.avatar) {
        localStorage.setItem('avatar', this.userInfo.avatar)
        this.userAvatar = this.userInfo.avatar
      } else {
        // 后端没有头像，尝试从localStorage读取
        this.userAvatar = localStorage.getItem('avatar') || ''
      }
      await this.loadCrops()
      this.loadUserCrops()
    },
    async loadUserInfo() {
      if (!this.userId) return
      try {
        const res = await getUserById(this.userId)
        console.log('用户信息:', res)
        if (res.code === 0) {
          this.userInfo = res.data || {}
          this.editForm.username = this.userInfo.username || ''
          this.editForm.phoneNumber = this.userInfo.phoneNumber || ''
        }
      } catch (e) {
        console.error('加载用户信息失败', e)
      }
    },
    async loadUserCrops() {
      if (!this.userId) return
      this.loadingCrops = true
      try {
        const res = await getUserCropsByUserId(this.userId)
        console.log('用户作物数据:', res)
        if (res.code === 0) {
          // 后端已返回 cropName 和 scientificName，直接使用
          this.userCrops = res.data || []
        }
      } catch (e) {
        console.error('加载用户作物失败', e)
      } finally {
        this.loadingCrops = false
      }
    },
    async loadCrops() {
      try {
        const res = await getAllCrops()
        console.log('作物列表:', res)
        if (res.code === 0) {
          this.crops = res.data || []
        }
      } catch (e) {
        console.error('加载作物列表失败', e)
      }
    },
    startEdit() {
      this.editing = true
      this.editForm.username = this.userInfo.username || ''
      this.editForm.phoneNumber = this.userInfo.phoneNumber || ''
    },
    cancelEdit() {
      this.editing = false
      this.avatarFile = null
    },
    async saveEdit() {
      if (!this.userId) return
      try {
        console.log('开始保存，avatarFile:', this.avatarFile)
        const res = await updateUser(this.userId, {
          username: this.editForm.username,
          phoneNumber: this.editForm.phoneNumber,
          avatar: this.avatarFile
        })
        console.log('updateUser返回:', res)
        if (res.code === 0) {
          this.$toast.success('修改成功')
          this.editing = false
          // 更新本地存储的用户名
          localStorage.setItem('username', this.editForm.username)
          this.username = this.editForm.username
          this.avatarFile = null
          // 重新从后端加载用户信息，确保获取最新的头像
          await this.loadUserInfo()
          console.log('loadUserInfo后userInfo:', this.userInfo)
          // 更新头像显示和localStorage
          if (this.userInfo.avatar) {
            localStorage.setItem('avatar', this.userInfo.avatar)
            this.userAvatar = this.userInfo.avatar
          }
        } else {
          console.error('返回错误:', res)
          this.$toast.error(res.message || '修改失败')
        }
      } catch (e) {
        console.error('saveEdit异常:', e)
        this.$toast.error('修改失败: ' + (e.message || '网络错误'))
      }
    },
    async handleAvatarChange(e) {
      const file = e.target.files[0]
      if (file) {
        // 预览
        const reader = new FileReader()
        reader.onload = (ev) => {
          this.userAvatar = ev.target.result
        }
        reader.readAsDataURL(file)
        // 直接上传更新数据库
        if (!this.userId) return
        try {
          const res = await updateUser(this.userId, { avatar: file })
          if (res.code === 0) {
            this.$toast.success('头像更新成功')
            await this.loadUserInfo()
            if (this.userInfo.avatar) {
              localStorage.setItem('avatar', this.userInfo.avatar)
              this.userAvatar = this.userInfo.avatar
            }
          } else {
            this.$toast.error(res.message || '头像更新失败')
          }
        } catch (err) {
          this.$toast.error('头像更新失败')
        }
      }
    },
    openAddCropModal() {
      this.addCropModalOpen = true
      this.cropMenuOpen = false
      this.selectedCropId = this.crops[0]?.id || null
    },
    closeAddCropModal() {
      this.addCropModalOpen = false
      this.cropMenuOpen = false
    },
    selectCrop(id) {
      this.selectedCropId = id
      this.cropMenuOpen = false
    },
    handleOutsideClick(e) {
      if (this.addCropModalOpen && !e.target.closest('.pseudo-select')) {
        this.cropMenuOpen = false
      }
    },
    async confirmAddCrop() {
      if (!this.userId || !this.selectedCropId) return
      try {
        const res = await addUserCrop(this.userId, this.selectedCropId)
        if (res.code === 0) {
          this.$toast.success('添加成功')
          this.closeAddCropModal()
          await this.loadUserCrops()
        } else {
          this.$toast.error(res.message || '添加失败')
        }
      } catch (e) {
        this.$toast.error('添加失败')
      }
    },
    async removeCrop(associationId) {
      try {
        const res = await deleteUserCrop(associationId)
        if (res.code === 0) {
          this.$toast.success('移除成功')
          this.userCrops = this.userCrops.filter(item => item.associationId !== associationId)
        } else {
          this.$toast.error(res.message || '移除失败')
        }
      } catch (e) {
        this.$toast.error('移除失败')
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.user-center {
  --panel: rgba(23, 28, 40, 0.9);
  --panel-soft: rgba(30, 36, 50, 0.9);
  --line: #3f2f1f;
  --accent: #ffd46a;
  --text: #f7e5be;
  --muted: #b8a98f;
  min-height: 100vh;
  padding-top: 80px;
  background:
    linear-gradient(rgba(9, 11, 18, 0.58), rgba(9, 11, 18, 0.58)),
    linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  font-family: 'Courier New', 'Lucida Console', monospace;
  color: var(--text);
  image-rendering: pixelated;
}

.user-main {
  width: min(800px, 94%);
  margin: 0 auto;
  padding: 20px;
}

/* 用户信息卡片 */
.user-profile {
  border: 2px solid var(--line);
  background: var(--panel);
  padding: 20px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 8px 0 rgba(8, 10, 15, 0.42);
}

.profile-header {
  padding-bottom: 12px;
  border-bottom: 2px solid var(--line);
}

.profile-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
}

.profile-card {
  margin-top: 16px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.avatar-section {
  flex: 0 0 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 4px 0 #1a2230;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  image-rendering: pixelated;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #8f7656 0%, #5c472f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder .avatar-text {
  font-size: 36px;
  font-weight: 700;
  color: #f6e5bf;
}

.avatar-upload-btn {
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f5e6cc;
  font-size: 11px;
  padding: 6px 12px;
  cursor: pointer;
  letter-spacing: 1px;
  text-align: center;
  display: inline-block;
}

.avatar-upload-btn:hover {
  background: #333a45;
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-label {
  flex: 0 0 80px;
  font-size: 12px;
  font-weight: 700;
  color: #d5ae63;
  letter-spacing: 1px;
}

.info-value-wrapper {
  flex: 1;
}

.info-value {
  font-size: 14px;
  color: var(--text);
}

.info-input {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #2a1c12;
  border-radius: 1px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #f5e6cc;
  background: #2b3038;
  outline: none;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
}

.info-input:focus {
  border-color: #8d6b4b;
  background: #333a45;
}

.role-badge {
  font-size: 12px;
  background: rgba(255, 212, 106, 0.1);
  border: 1px solid rgba(255, 212, 106, 0.3);
  padding: 4px 8px;
  color: var(--accent);
}

.profile-actions {
  margin-top: 16px;
  display: flex;
  gap: 10px;
}

.action-btn {
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f5e6cc;
  font-size: 12px;
  padding: 8px 16px;
  cursor: pointer;
  letter-spacing: 1px;
}

.action-btn:hover {
  background: #333a45;
}

.action-btn.primary {
  background: #8d6b4b;
  color: #fff;
}

/* 用户作物 */
.user-crops {
  margin-top: 20px;
  border: 2px solid var(--line);
  background: var(--panel-soft);
  padding: 20px;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.07), 0 6px 0 rgba(8, 10, 15, 0.35);
}

.crops-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--line);
}

.crops-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ffe5a8;
}

.add-btn {
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f5e6cc;
  font-size: 12px;
  padding: 6px 12px;
  cursor: pointer;
}

.add-btn:hover {
  background: #333a45;
}

.crops-loading,
.crops-empty {
  padding: 20px;
  text-align: center;
  color: var(--muted);
  font-size: 13px;
}

.crops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.crop-card {
  border: 2px solid #65462a;
  background: #252c3a;
  box-shadow: 0 4px 0 #1a2230;
  padding: 12px;
}

.crop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(101, 70, 42, 0.7);
}

.crop-name {
  font-size: 14px;
  font-weight: 700;
  color: #ffe5a8;
}

.crop-remove-btn {
  border: 1px solid #6c4d26;
  background: transparent;
  color: #ffb0a4;
  font-size: 11px;
  padding: 4px 8px;
  cursor: pointer;
}

.crop-remove-btn:hover {
  background: rgba(255, 176, 164, 0.1);
}

.crop-desc {
  margin-top: 8px;
  font-size: 12px;
  color: var(--muted);
}

.crop-time {
  margin-top: 6px;
  font-size: 11px;
  color: #8a7a68;
}

/* 弹窗 */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(12, 14, 22, 0.58);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 80;
}

.modal-content {
  width: min(400px, calc(100vw - 24px));
  border: 2px solid #2a1c12;
  background: #252c3a;
  box-shadow: 0 12px 0 rgba(0, 0, 0, 0.32);
  padding: 16px;
}

.modal-title {
  font-size: 14px;
  color: #f5e6cc;
  letter-spacing: 1px;
  padding-bottom: 12px;
  border-bottom: 2px solid #2a1c12;
}

.modal-field {
  margin-top: 12px;
}

.modal-label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #f5e6cc;
  margin-bottom: 6px;
  letter-spacing: 1px;
}

.pseudo-select {
  position: relative;
}

.select-trigger {
  width: 100%;
  text-align: left;
  border: 2px solid #2a1c12;
  border-radius: 1px;
  background: #2b3038;
  color: #f5e6cc;
  padding: 10px 36px 10px 14px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  cursor: pointer;
  outline: none;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.35);
  position: relative;
}

.select-trigger::after {
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

.select-menu {
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

.select-menu li {
  padding: 10px 12px;
  cursor: pointer;
  color: #f5e6cc;
}

.select-menu li:hover {
  background: #333a45;
}

.modal-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.modal-btn {
  border: 2px solid #65462a;
  background: #2b3038;
  color: #f5e6cc;
  font-size: 12px;
  padding: 8px 16px;
  cursor: pointer;
}

.modal-btn:hover {
  background: #333a45;
}

.modal-btn.primary {
  background: #8d6b4b;
  color: #fff;
}

/* 浅色模式 */
.user-center.light-mode {
  --panel: rgba(255, 249, 238, 0.9);
  --panel-soft: rgba(250, 242, 230, 0.92);
  --line: #9a7348;
  --accent: #a86820;
  --text: #3f2c1f;
  --muted: #564636;
  background:
    linear-gradient(rgba(255, 248, 236, 0), rgba(255, 248, 236, 0)),
    linear-gradient(rgba(66, 49, 32, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(66, 49, 32, 0.07) 1px, transparent 1px);
  background-size: auto, 8px 8px, 8px 8px;
  color: var(--text);
}

.user-center.light-mode .profile-title,
.user-center.light-mode .crops-title {
  color: #5f3c1e;
}

.user-center.light-mode .profile-card,
.user-center.light-mode .crop-card {
  background: #f8f0e2;
  border-color: #9a7348;
}

.user-center.light-mode .avatar-wrapper {
  border-color: #9a7348;
  background: #f8f0e2;
}

.user-center.light-mode .avatar-placeholder {
  background: linear-gradient(180deg, #dac5a7 0%, #b7956f 100%);
}

.user-center.light-mode .avatar-placeholder .avatar-text {
  color: #5f3c1e;
}

.user-center.light-mode .avatar-upload-btn,
.user-center.light-mode .action-btn,
.user-center.light-mode .add-btn,
.user-center.light-mode .modal-btn {
  background: #f1e9db;
  border-color: #9a7348;
  color: #5f3c1e;
}

.user-center.light-mode .avatar-upload-btn:hover,
.user-center.light-mode .action-btn:hover,
.user-center.light-mode .add-btn:hover,
.user-center.light-mode .modal-btn:hover {
  background: #ece1d0;
}

.user-center.light-mode .action-btn.primary,
.user-center.light-mode .modal-btn.primary {
  background: #9a7348;
  color: #fff;
}

.user-center.light-mode .info-label {
  color: #8b5f2e;
}

.user-center.light-mode .info-value {
  color: var(--text);
}

.user-center.light-mode .info-input {
  background: #f1e9db;
  border-color: #9a7348;
  color: #5f3c1e;
}

.user-center.light-mode .info-input:focus {
  background: #ece1d0;
  border-color: #6f4c30;
}

.user-center.light-mode .role-badge {
  background: rgba(168, 104, 32, 0.12);
  border-color: rgba(154, 115, 72, 0.45);
  color: #8b5a1e;
}

.user-center.light-mode .crop-name {
  color: #5f3c1e;
}

.user-center.light-mode .crop-remove-btn {
  color: #8e3f31;
}

.user-center.light-mode .crop-desc,
.user-center.light-mode .crop-time {
  color: #564636;
}

.user-center.light-mode .modal-content {
  background: #f8f0e2;
  border-color: #9a7348;
}

.user-center.light-mode .modal-title,
.user-center.light-mode .modal-label {
  color: #5f3c1e;
}

.user-center.light-mode .select-trigger,
.user-center.light-mode .select-menu,
.user-center.light-mode .select-menu li {
  background: #f1e9db;
  border-color: #9a7348;
  color: #5f3c1e;
}

.user-center.light-mode .select-menu li:hover {
  background: #ece1d0;
}

@media (max-width: 680px) {
  .profile-card {
    flex-direction: column;
    align-items: center;
  }

  .avatar-section {
    flex: none;
  }

  .profile-info {
    width: 100%;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }

  .info-label {
    flex: none;
  }

  .profile-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>