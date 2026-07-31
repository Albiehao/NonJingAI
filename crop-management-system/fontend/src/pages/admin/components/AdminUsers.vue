<template>
  <section class="admin-panel">
    <div class="admin-panel-head admin-panel-head--rich">
      <div>
        <h3 class="admin-panel-title">用户管理</h3>
        <p class="panel-subtitle">集中维护账号、手机号和角色信息。</p>
      </div>
      <button type="button" class="admin-btn" @click="openCreate">新增用户</button>
    </div>

    <admin-table-scroll>
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>手机号</th>
            <th>角色</th>
            <th>注册时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in users" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.username }}</td>
            <td>{{ item.phoneNumber || '-' }}</td>
            <td><span class="role-chip">{{ normalizeRole(item.role) }}</span></td>
            <td>{{ item.createdAt || '-' }}</td>
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

    <div v-if="editingUser" class="admin-modal-mask" @click.self="closeEdit">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">编辑用户</h4>
          <label class="admin-modal-field">
            <span>用户名</span>
            <input v-model.trim="form.username" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>手机号</span>
            <input v-model.trim="form.phoneNumber" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>角色</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="roleMenuOpen = !roleMenuOpen">
                {{ form.role }}
              </button>
              <ul v-if="roleMenuOpen" class="admin-select-menu">
                <li @click="setRole('USER')">USER</li>
                <li @click="setRole('ADMIN')">ADMIN</li>
                <li @click="setRole('FARMER')">FARMER</li>
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

    <div v-if="creatingUser" class="admin-modal-mask" @click.self="closeCreate">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">新增用户</h4>
          <label class="admin-modal-field">
            <span>用户名</span>
            <input v-model.trim="createForm.username" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>手机号</span>
            <input v-model.trim="createForm.phoneNumber" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>角色</span>
            <div class="admin-pseudo-select">
              <button type="button" class="admin-select-trigger" @click="createRoleMenuOpen = !createRoleMenuOpen">
                {{ createForm.role }}
              </button>
              <ul v-if="createRoleMenuOpen" class="admin-select-menu">
                <li @click="setCreateRole('USER')">USER</li>
                <li @click="setCreateRole('ADMIN')">ADMIN</li>
                <li @click="setCreateRole('FARMER')">FARMER</li>
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
  name: 'AdminUsers',
  components: {
    AdminTableScroll
  },
  props: {
    users: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingUser: null,
      creatingUser: false,
      form: {
        username: '',
        phoneNumber: '',
        role: 'USER'
      },
      roleMenuOpen: false,
      createForm: {
        username: '',
        phoneNumber: '',
        role: 'USER'
      },
      createRoleMenuOpen: false
    }
  },
  methods: {
    normalizeRole(role) {
      if (role === 'ADMIN') return 'ADMIN'
      if (role === 'FARMER') return 'FARMER'
      return 'USER'
    },
    openEdit(user) {
      this.editingUser = user
      this.form = {
        username: user.username,
        phoneNumber: user.phoneNumber || '',
        role: this.normalizeRole(user.role),
        createdAt: user.createdAt
      }
      this.roleMenuOpen = false
    },
    openCreate() {
      this.creatingUser = true
      this.createForm = {
        username: '',
        phoneNumber: '',
        role: 'USER'
      }
      this.createRoleMenuOpen = false
    },
    closeCreate() {
      this.creatingUser = false
      this.createRoleMenuOpen = false
    },
    closeEdit() {
      this.editingUser = null
      this.roleMenuOpen = false
    },
    setRole(value) {
      this.form.role = this.normalizeRole(value)
      this.roleMenuOpen = false
    },
    setCreateRole(value) {
      this.createForm.role = this.normalizeRole(value)
      this.createRoleMenuOpen = false
    },
    saveCreate() {
      const username = this.createForm.username.trim()
      const phoneNumber = this.createForm.phoneNumber.trim()
      const role = this.normalizeRole(this.createForm.role)
      if (!username || !role) return
      this.$emit('add', {
        username,
        phoneNumber,
        role,
        createdAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeCreate()
    },
    saveEdit() {
      if (!this.editingUser) return
      const username = this.form.username.trim()
      const phoneNumber = this.form.phoneNumber.trim()
      const role = this.normalizeRole(this.form.role)
      if (!username || !role) return
      this.$emit('edit', {
        id: this.editingUser.id,
        username,
        phoneNumber,
        role,
        createdAt: this.editingUser.createdAt
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

.role-chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  background: rgba(255, 207, 106, 0.14);
  color: var(--admin-accent);
  font-size: 12px;
  font-weight: 700;
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
  width: min(440px, calc(100vw - 24px));
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
  max-height: 220px;
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
