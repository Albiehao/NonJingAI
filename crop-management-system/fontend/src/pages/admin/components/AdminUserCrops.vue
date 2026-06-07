<template>
  <section class="admin-panel">
    <div class="admin-panel-head admin-panel-head--rich">
      <div>
        <h3 class="admin-panel-title">用户作物关联</h3>
        <p class="panel-subtitle">管理用户与种植作物之间的对应关系。</p>
      </div>
      <button type="button" class="admin-btn" @click="openCreate">新增关联</button>
    </div>

    <admin-table-scroll>
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户</th>
            <th>作物</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.username || `用户(${item.userId})` }}</td>
            <td>{{ item.cropName || `作物(${item.cropId})` }}</td>
            <td>{{ item.updatedAt || '-' }}</td>
            <td>
              <div class="table-actions">
                <button type="button" class="admin-btn" @click="openEdit(item)">编辑</button>
                <button type="button" class="admin-btn danger" @click="$emit('remove', item.id)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </admin-table-scroll>

    <div v-if="editingItem" class="admin-modal-mask" @click.self="closeEdit">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">编辑关联</h4>
          <label class="admin-modal-field">
            <span>选择用户</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="editUserMenuOpen = !editUserMenuOpen">
                {{ usernameById(form.userId) }}
              </button>
              <ul v-if="editUserMenuOpen" class="admin-select-menu">
                <li v-for="u in users" :key="u.id" @click="setEditUser(u.id)">{{ u.username }}</li>
              </ul>
            </div>
          </label>
          <label class="admin-modal-field">
            <span>选择作物</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="editCropMenuOpen = !editCropMenuOpen">
                {{ cropNameById(form.cropId) }}
              </button>
              <ul v-if="editCropMenuOpen" class="admin-select-menu">
                <li v-for="c in crops" :key="c.id" @click="setEditCrop(c.id)">{{ c.name }}</li>
              </ul>
            </div>
          </label>
        </div>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="saveEdit">保存</button>
          <button type="button" class="admin-btn danger" @click="closeEdit">取消</button>
        </div>
      </div>
    </div>

    <div v-if="creatingItem" class="admin-modal-mask" @click.self="closeCreate">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">新增关联</h4>
          <label class="admin-modal-field">
            <span>选择用户</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="createUserMenuOpen = !createUserMenuOpen">
                {{ usernameById(createForm.userId) }}
              </button>
              <ul v-if="createUserMenuOpen" class="admin-select-menu">
                <li v-for="u in users" :key="u.id" @click="setCreateUser(u.id)">{{ u.username }}</li>
              </ul>
            </div>
          </label>
          <label class="admin-modal-field">
            <span>选择作物</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="createCropMenuOpen = !createCropMenuOpen">
                {{ cropNameById(createForm.cropId) }}
              </button>
              <ul v-if="createCropMenuOpen" class="admin-select-menu">
                <li v-for="c in crops" :key="c.id" @click="setCreateCrop(c.id)">{{ c.name }}</li>
              </ul>
            </div>
          </label>
        </div>
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
  name: 'AdminUserCrops',
  components: {
    AdminTableScroll
  },
  props: {
    items: {
      type: Array,
      default: () => []
    },
    users: {
      type: Array,
      default: () => []
    },
    crops: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingItem: null,
      creatingItem: false,
      editUserMenuOpen: false,
      editCropMenuOpen: false,
      createUserMenuOpen: false,
      createCropMenuOpen: false,
      form: {
        userId: 1,
        cropId: 1
      },
      createForm: {
        userId: 1,
        cropId: 1
      }
    }
  },
  methods: {
    usernameById(userId) {
      const user = this.users.find(u => u.id === userId)
      return user ? user.username : `用户(${userId})`
    },
    cropNameById(cropId) {
      const crop = this.crops.find(c => c.id === cropId)
      return crop ? crop.name : `作物(${cropId})`
    },
    openEdit(item) {
      this.editingItem = item
      this.form = {
        userId: item.userId,
        cropId: item.cropId
      }
      this.editUserMenuOpen = false
      this.editCropMenuOpen = false
    },
    openCreate() {
      this.creatingItem = true
      this.createForm = {
        userId: this.users[0] ? this.users[0].id : 1,
        cropId: this.crops[0] ? this.crops[0].id : 1
      }
      this.createUserMenuOpen = false
      this.createCropMenuOpen = false
    },
    closeCreate() {
      this.creatingItem = false
      this.createUserMenuOpen = false
      this.createCropMenuOpen = false
    },
    setEditUser(id) {
      this.form.userId = Number(id)
      this.editUserMenuOpen = false
    },
    setEditCrop(id) {
      this.form.cropId = Number(id)
      this.editCropMenuOpen = false
    },
    setCreateUser(id) {
      this.createForm.userId = Number(id)
      this.createUserMenuOpen = false
    },
    setCreateCrop(id) {
      this.createForm.cropId = Number(id)
      this.createCropMenuOpen = false
    },
    saveCreate() {
      const userId = Number(this.createForm.userId)
      const cropId = Number(this.createForm.cropId)
      if (!Number.isFinite(userId) || userId <= 0) return
      if (!Number.isFinite(cropId) || cropId <= 0) return
      this.$emit('add', {
        userId,
        cropId
      })
      this.closeCreate()
    },
    closeEdit() {
      this.editingItem = null
      this.editUserMenuOpen = false
      this.editCropMenuOpen = false
    },
    saveEdit() {
      if (!this.editingItem) return
      const userId = Number(this.form.userId)
      const cropId = Number(this.form.cropId)
      if (!Number.isFinite(userId) || userId <= 0) return
      if (!Number.isFinite(cropId) || cropId <= 0) return
      this.$emit('edit', {
        id: this.editingItem.id,
        userId,
        cropId
      })
      this.closeEdit()
    }
  }
}
</script>

<style scoped>
.admin-panel-head--rich {
  align-items: flex-start;
}

.panel-subtitle {
  margin-top: 6px;
  color: var(--admin-sub-text);
  font-size: 12px;
  line-height: 1.6;
}

.table-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.admin-modal-mask {
  position: fixed;
  inset: 0;
  padding: 24px;
  background: rgba(12, 14, 22, 0.58);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: auto;
  z-index: 80;
}

.admin-modal {
  width: min(460px, calc(100vw - 24px));
  max-height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 2px solid #2a1c12;
  background: #252c3a;
  box-shadow: 0 12px 0 rgba(0, 0, 0, 0.32);
}

.admin-modal-body {
  padding: 16px;
  overflow: auto;
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

.admin-modal-actions {
  padding: 14px 16px 16px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(24, 31, 43, 0.92);
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
  max-height: 240px;
  overflow: auto;
  border: 2px solid #2a1c12;
  background: #2b3038;
  box-shadow: 0 6px 0 rgba(0, 0, 0, 0.28);
  z-index: 6;
}

.admin-select-menu li {
  padding: 10px 12px;
  cursor: pointer;
  color: #f5e6cc;
}

.admin-select-menu li:hover {
  background: #333a45;
}

@media (max-width: 760px) {
  .admin-modal-mask {
    padding: 12px;
    align-items: flex-end;
  }

  .admin-modal {
    width: 100%;
    max-height: calc(100vh - 24px);
  }
}
</style>
