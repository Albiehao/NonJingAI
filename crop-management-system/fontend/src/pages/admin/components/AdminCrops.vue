<template>
  <section class="admin-panel">
    <div class="admin-panel-head admin-panel-head--rich">
      <div>
        <h3 class="admin-panel-title">农作物管理</h3>
        <p class="panel-subtitle">维护作物名称与学名，供商品和用户种植信息引用。</p>
      </div>
      <button type="button" class="admin-btn" @click="openCreate">新增农作物</button>
    </div>

    <admin-table-scroll>
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>通用名</th>
            <th>学名</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in crops" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.scientificName }}</td>
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

    <div v-if="editingCrop" class="admin-modal-mask" @click.self="closeEdit">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">编辑农作物</h4>
          <label class="admin-modal-field">
            <span>作物名称</span>
            <input v-model.trim="form.name" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>学名</span>
            <input v-model.trim="form.scientificName" type="text" />
          </label>
        </div>
        <div class="admin-modal-actions">
          <button type="button" class="admin-btn" @click="saveEdit">保存</button>
          <button type="button" class="admin-btn danger" @click="closeEdit">取消</button>
        </div>
      </div>
    </div>

    <div v-if="creatingCrop" class="admin-modal-mask" @click.self="closeCreate">
      <div class="admin-modal">
        <div class="admin-modal-body">
          <h4 class="admin-modal-title">新增农作物</h4>
          <label class="admin-modal-field">
            <span>作物名称</span>
            <input v-model.trim="createForm.name" type="text" />
          </label>
          <label class="admin-modal-field">
            <span>学名</span>
            <input v-model.trim="createForm.scientificName" type="text" />
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
  name: 'AdminCrops',
  components: {
    AdminTableScroll
  },
  props: {
    crops: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingCrop: null,
      creatingCrop: false,
      form: {
        name: '',
        scientificName: ''
      },
      createForm: {
        name: '',
        scientificName: ''
      }
    }
  },
  methods: {
    openEdit(crop) {
      this.editingCrop = crop
      this.form = {
        name: crop.name,
        scientificName: crop.scientificName
      }
    },
    openCreate() {
      this.creatingCrop = true
      this.createForm = {
        name: '',
        scientificName: ''
      }
    },
    closeCreate() {
      this.creatingCrop = false
    },
    saveCreate() {
      const name = this.createForm.name.trim()
      const scientificName = this.createForm.scientificName.trim()
      if (!name || !scientificName) return
      this.$emit('add', {
        name,
        scientificName,
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      this.closeCreate()
    },
    closeEdit() {
      this.editingCrop = null
    },
    saveEdit() {
      if (!this.editingCrop) return
      const name = this.form.name.trim()
      const scientificName = this.form.scientificName.trim()
      if (!name || !scientificName) return
      this.$emit('edit', {
        id: this.editingCrop.id,
        name,
        scientificName,
        updatedAt: new Date().toISOString().slice(0, 19).replace('T', ' ')
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
