<template>
  <section class="admin-panel">
    <div class="admin-panel-head">
      <h3 class="admin-panel-title">农资分类管理</h3>
      <button type="button" class="admin-btn" @click="openCreate">新增分类</button>
    </div>
    <admin-table-scroll>
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>分类名称</th>
            <th>父分类</th>
            <th>分类描述</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in displayCategories" :key="item.id">
            <td>{{ item.id }}</td>
            <td class="cat-name" :style="{ paddingLeft: `${10 + item.level * 18}px` }">
              <span v-if="item.level === 1" class="cat-branch">└</span>{{ item.name }}
            </td>
            <td>{{ item.parentName || (item.parentId == null ? 'ROOT' : item.parentId) }}</td>
            <td>{{ item.description || '-' }}</td>
            <td>{{ item.updatedAt || '-' }}</td>
            <td>
              <button type="button" class="admin-btn" @click="openEdit(item)">编辑</button>
              <button type="button" class="admin-btn danger" @click="$emit('remove', item.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </admin-table-scroll>

    <div v-if="editingCategory" class="admin-modal-mask" @click.self="closeEdit">
      <div class="admin-modal">
        <h4 class="admin-modal-title">编辑分类</h4>
        <label class="admin-modal-field">
          <span>分类名称</span>
          <input v-model.trim="form.name" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>父分类（可选二级）</span>
          <div class="admin-pseudo-select">
            <button type="button" class="admin-select-trigger" @click="parentMenuOpen = !parentMenuOpen">
              {{ parentLabel(form.parentId) }}
            </button>
            <ul v-if="parentMenuOpen" class="admin-select-menu">
              <li @click="setParent('edit', null)">ROOT（顶级）</li>
              <li v-for="p in parentOptions" :key="p.id" @click="setParent('edit', p.id)">
                {{ p.name }}
              </li>
            </ul>
          </div>
        </label>
        <label class="admin-modal-field">
          <span>分类描述</span>
          <input v-model.trim="form.description" type="text" />
        </label>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="saveEdit">保存</button>
          <button type="button" class="admin-btn danger" @click="closeEdit">取消</button>
        </div>
      </div>
    </div>
    <div v-if="creatingCategory" class="admin-modal-mask" @click.self="closeCreate">
      <div class="admin-modal">
        <h4 class="admin-modal-title">新增分类</h4>
        <label class="admin-modal-field">
          <span>分类名称</span>
          <input v-model.trim="createForm.name" type="text" />
        </label>
        <label class="admin-modal-field">
          <span>父分类（可选二级）</span>
          <div class="admin-pseudo-select">
            <button type="button" class="admin-select-trigger" @click="createParentMenuOpen = !createParentMenuOpen">
              {{ parentLabel(createForm.parentId) }}
            </button>
            <ul v-if="createParentMenuOpen" class="admin-select-menu">
              <li @click="setParent('create', null)">ROOT（顶级）</li>
              <li v-for="p in parentOptions" :key="p.id" @click="setParent('create', p.id)">
                {{ p.name }}
              </li>
            </ul>
          </div>
        </label>
        <label class="admin-modal-field">
          <span>分类描述</span>
          <input v-model.trim="createForm.description" type="text" />
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
  name: 'AdminCategories',
  components: {
    AdminTableScroll
  },
  props: {
    categories: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingCategory: null,
      creatingCategory: false,
      parentMenuOpen: false,
      createParentMenuOpen: false,
      form: {
        name: '',
        parentId: null,
        description: ''
      },
      createForm: {
        name: '',
        parentId: null,
        description: ''
      }
    }
  },
  computed: {
    roots() {
      return this.categories.filter(c => c.parentId == null)
    },
    parentOptions() {
      // 限制为二级分类：只允许选择一级分类作为父分类
      return this.roots.slice().sort((a, b) => String(a.name).localeCompare(String(b.name), 'zh-Hans-CN'))
    },
    displayCategories() {
      const byParent = new Map()
      const push = (pid, item) => {
        const key = pid == null ? null : pid
        if (!byParent.has(key)) byParent.set(key, [])
        byParent.get(key).push(item)
      }
      this.categories.forEach(c => push(c.parentId, c))
      const sort = (a, b) => String(a.name).localeCompare(String(b.name), 'zh-Hans-CN')
      const roots = (byParent.get(null) || []).slice().sort(sort)
      const result = []
      roots.forEach(r => {
        result.push({ ...r, level: 0, parentName: '' })
        const children = (byParent.get(r.id) || []).slice().sort(sort)
        children.forEach(ch => {
          result.push({ ...ch, level: 1, parentName: r.name })
        })
      })
      return result
    }
  },
  methods: {
    openEdit(category) {
      this.editingCategory = category
      this.form = {
        name: category.name,
        parentId: category.parentId == null ? null : category.parentId,
        description: category.description || ''
      }
      this.parentMenuOpen = false
    },
    openCreate() {
      this.creatingCategory = true
      this.createForm = {
        name: '',
        parentId: null,
        description: ''
      }
      this.createParentMenuOpen = false
    },
    closeCreate() {
      this.creatingCategory = false
      this.createParentMenuOpen = false
    },
    saveCreate() {
      const name = this.createForm.name.trim()
      const description = this.createForm.description.trim()
      if (!name) return
      this.$emit('add', {
        name,
        parentId: this.createForm.parentId,
        description,
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeCreate()
    },
    closeEdit() {
      this.editingCategory = null
      this.parentMenuOpen = false
    },
    setParent(mode, value) {
      if (mode === 'edit') {
        this.form.parentId = value
        this.parentMenuOpen = false
        return
      }
      this.createForm.parentId = value
      this.createParentMenuOpen = false
    },
    parentLabel(parentId) {
      if (parentId == null) return 'ROOT（顶级）'
      const found = this.categories.find(c => c.id === parentId)
      return found ? found.name : String(parentId)
    },
    saveEdit() {
      if (!this.editingCategory) return
      const name = this.form.name.trim()
      const description = this.form.description.trim()
      if (!name) return
      this.$emit('edit', {
        id: this.editingCategory.id,
        name,
        parentId: this.form.parentId,
        description,
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeEdit()
    }
  }
}
</script>

<style scoped>
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
  width: min(420px, calc(100vw - 24px));
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

.cat-name {
  position: relative;
}

.cat-branch {
  margin-right: 6px;
  color: rgba(255, 212, 106, 0.7);
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
  max-height: 220px;
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.admin-select-menu::-webkit-scrollbar {
  width: 0;
  height: 0;
  display: none;
}

.admin-select-menu li {
  padding: 10px 12px;
  cursor: pointer;
  color: #f5e6cc;
}

.admin-select-menu li:hover {
  background: #333a45;
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
</style>

