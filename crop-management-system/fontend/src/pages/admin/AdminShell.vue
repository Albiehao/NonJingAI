<template>
  <div class="admin-page" :class="{ 'light-mode': isLightMode }">
    <div class="admin-container">
      <admin-sidebar
        :menus="menus"
        :current-menu="currentMenu"
        :mobile-open="mobileNavOpen"
        @select="handleMenuSelect"
        @toggle-mobile="mobileNavOpen = !mobileNavOpen"
      />
      <div class="admin-main">
        <admin-topbar :title="currentMenuLabel" :username="username" />
        <section class="admin-content">
          <admin-dashboard
            v-if="currentMenu === 'dashboard'"
            :users-count="users.length"
            :categories-count="categories.length"
            :products-count="products.length"
            :crops-count="crops.length"
            :total-stock="totalStock"
          />
          <admin-users
            v-else-if="currentMenu === 'users'"
            :users="users"
            @add="addUser"
            @edit="editUser"
            @remove="removeUser"
          />
          <admin-categories
            v-else-if="currentMenu === 'categories'"
            :categories="categories"
            @add="addCategory"
            @edit="editCategory"
            @remove="removeCategory"
          />
          <admin-products
            v-else-if="currentMenu === 'products'"
            :products="products"
            :categories="categories"
            @add="addProduct"
            @edit="editProduct"
            @remove="removeProduct"
          />
          <admin-crops
            v-else-if="currentMenu === 'crops'"
            :crops="crops"
            @add="addCrop"
            @edit="editCrop"
            @remove="removeCrop"
          />
          <admin-user-crops
            v-else
            :items="userCropsWithNames"
            :users="users"
            :crops="crops"
            @add="addUserCrop"
            @edit="editUserCrop"
            @remove="removeUserCrop"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import './adminTheme.css'
import AdminSidebar from './components/AdminSidebar.vue'
import AdminTopbar from './components/AdminTopbar.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import AdminUsers from './components/AdminUsers.vue'
import AdminCategories from './components/AdminCategories.vue'
import AdminProducts from './components/AdminProducts.vue'
import AdminCrops from './components/AdminCrops.vue'
import AdminUserCrops from './components/AdminUserCrops.vue'
import { getAllUsers, register, updateUser, deleteUser } from '@/api/user'
import { getAllCrops, addCrop, updateCrop, deleteCrop } from '@/api/crops'
import { getAllCategories } from '@/api/categories'
import { getAllAgrochemicals, addAgrochemical, updateAgrochemical, deleteAgrochemical } from '@/api/agrochemicals'
import { getAllUserCrops, addUserCrop, updateUserCrop, deleteUserCrop } from '@/api/userCrops'

export default {
  name: 'AdminShell',
  components: {
    AdminSidebar,
    AdminTopbar,
    AdminDashboard,
    AdminUsers,
    AdminCategories,
    AdminProducts,
    AdminCrops,
    AdminUserCrops
  },
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tempIdSeed: -1,
      mobileNavOpen: false,
      currentMenu: 'dashboard',
      menus: [
        { key: 'dashboard', label: '看板' },
        { key: 'users', label: '用户管理' },
        { key: 'categories', label: '农资分类管理' },
        { key: 'products', label: '农资商品管理' },
        { key: 'crops', label: '农作物管理' },
        { key: 'userCrops', label: '用户作物关联' }
      ],
      users: [],
      categories: [],
      products: [],
      crops: [],
      userCrops: []
    }
  },
  async mounted() {
    await this.loadUsers()
    await this.loadCrops()
    await this.loadCategories()
    await this.loadProducts()
    await this.loadUserCrops()
  },
  computed: {
    isLightMode() {
      return this.globalLightMode
    },
    username() {
      return (localStorage.getItem('username') || '管理员').trim() || '管理员'
    },
    currentMenuLabel() {
      const found = this.menus.find(item => item.key === this.currentMenu)
      return found ? found.label : '看板'
    },
    totalStock() {
      return this.userCrops.length
    },
    userCropsWithNames() {
      return this.userCrops.map(item => {
        const user = this.users.find(u => u.id === item.userId)
        const crop = this.crops.find(c => c.id === item.cropId)
        return {
          ...item,
          username: user?.username || '',
          cropName: crop?.name || ''
        }
      })
    }
  },
  methods: {
    handleMenuSelect(key) {
      this.currentMenu = key
      this.mobileNavOpen = false
    },
    async loadUsers() {
      try {
        const res = await getAllUsers()
        if (res.code === 0) this.users = res.data || []
      } catch (e) {
        console.error('加载用户列表失败', e)
      }
    },
    async loadCrops() {
      try {
        const res = await getAllCrops()
        if (res.code === 0) this.crops = res.data || []
      } catch (e) {
        console.error('加载作物列表失败', e)
      }
    },
    async loadCategories() {
      try {
        const res = await getAllCategories()
        if (res.code === 0) this.categories = res.data || []
      } catch (e) {
        console.error('加载分类列表失败', e)
      }
    },
    async loadProducts() {
      try {
        const res = await getAllAgrochemicals()
        if (res.code === 0) this.products = res.data || []
      } catch (e) {
        console.error('加载商品列表失败', e)
      }
    },
    async loadUserCrops() {
      try {
        const res = await getAllUserCrops()
        if (res.code === 0) this.userCrops = res.data || []
      } catch (e) {
        console.error('加载用户作物关联失败', e)
      }
    },
    async addUser(payload) {
      if (!payload || !payload.username) return
      try {
        const res = await register(payload.username, payload.username + '123456', payload.phoneNumber)
        if (res.code === 0) {
          await this.loadUsers()
          this.$toast.success('添加用户成功')
        } else {
          this.$toast.error(res.message || '添加用户失败')
        }
      } catch (e) {
        this.$toast.error('添加用户失败')
      }
    },
    async removeUser(id) {
      try {
        const res = await deleteUser(id)
        if (res.code === 0) {
          this.users = this.users.filter(item => item.id !== id)
          this.$toast.success('删除用户成功')
        } else {
          this.$toast.error(res.message || '删除用户失败')
        }
      } catch (e) {
        this.$toast.error('删除用户失败')
      }
    },
    async editUser(payload) {
      try {
        const res = await updateUser(payload.id, {
          username: payload.username,
          phoneNumber: payload.phoneNumber
        })
        if (res.code === 0) {
          await this.loadUsers()
          this.$toast.success('修改用户成功')
        } else {
          this.$toast.error(res.message || '修改用户失败')
        }
      } catch (e) {
        this.$toast.error('修改用户失败')
      }
    },
    addCategory(payload) {
      if (!payload || !payload.name) return
      const id = this.nextTempId()
      this.categories.push({
        id,
        name: payload.name,
        parentId: payload.parentId == null ? null : payload.parentId,
        description: payload.description || '',
        updatedAt: payload.updatedAt || this.now()
      })
      this.$toast.success('添加分类成功（本地）')
    },
    removeCategory(id) {
      this.categories = this.categories.filter(item => item.id !== id)
      this.$toast.success('删除分类成功（本地）')
    },
    editCategory(payload) {
      this.categories = this.categories.map(item => (item.id === payload.id ? { ...item, ...payload } : item))
      this.$toast.success('修改分类成功（本地）')
    },
    async addProduct(payload) {
      if (!payload || !payload.productName) return
      try {
        const res = await addAgrochemical({
          productName: payload.productName,
          categoryId: payload.categoryId,
          brand: payload.manufacturer,
          registrationNo: payload.registrationNo,
          formulation: payload.formulation,
          contentSpec: payload.contentSpec,
          useCrops: payload.useCrops,
          purchaseLinks: payload.purchaseLinks,
          mainImage: payload.mainImage,
          description: payload.description || ''
        })
        if (res.code === 0) {
          await this.loadProducts()
          this.$toast.success('添加商品成功')
        } else {
          this.$toast.error(res.message || '添加商品失败')
        }
      } catch (e) {
        this.$toast.error('添加商品失败')
      }
    },
    async removeProduct(id) {
      try {
        const res = await deleteAgrochemical(id)
        if (res.code === 0) {
          this.products = this.products.filter(item => item.id !== id)
          this.$toast.success('删除商品成功')
        } else {
          this.$toast.error(res.message || '删除商品失败')
        }
      } catch (e) {
        this.$toast.error('删除商品失败')
      }
    },
    async editProduct(payload) {
      try {
        const res = await updateAgrochemical({
          id: payload.id,
          productName: payload.productName,
          categoryId: payload.categoryId,
          brand: payload.manufacturer,
          registrationNo: payload.registrationNo,
          formulation: payload.formulation,
          contentSpec: payload.contentSpec,
          useCrops: payload.useCrops,
          purchaseLinks: payload.purchaseLinks,
          mainImage: payload.mainImage,
          description: payload.description || ''
        })
        if (res.code === 0) {
          await this.loadProducts()
          this.$toast.success('修改商品成功')
        } else {
          this.$toast.error(res.message || '修改商品失败')
        }
      } catch (e) {
        this.$toast.error('修改商品失败')
      }
    },
    async addCrop(payload) {
      if (!payload || !payload.name || !payload.scientificName) return
      try {
        const res = await addCrop(payload.name, payload.scientificName)
        if (res.code === 0) {
          await this.loadCrops()
          this.$toast.success('添加作物成功')
        } else {
          this.$toast.error(res.message || '添加作物失败')
        }
      } catch (e) {
        this.$toast.error('添加作物失败')
      }
    },
    async removeCrop(id) {
      try {
        const res = await deleteCrop(id)
        if (res.code === 0) {
          this.crops = this.crops.filter(item => item.id !== id)
          this.$toast.success('删除作物成功')
        } else {
          this.$toast.error(res.message || '删除作物失败')
        }
      } catch (e) {
        this.$toast.error('删除作物失败')
      }
    },
    async editCrop(payload) {
      try {
        const res = await updateCrop(payload.id, payload.name, payload.scientificName)
        if (res.code === 0) {
          await this.loadCrops()
          this.$toast.success('修改作物成功')
        } else {
          this.$toast.error(res.message || '修改作物失败')
        }
      } catch (e) {
        this.$toast.error('修改作物失败')
      }
    },
    async addUserCrop(payload) {
      if (!payload || !payload.userId || !payload.cropId) return
      try {
        const res = await addUserCrop(payload.userId, payload.cropId)
        if (res.code === 0) {
          await this.loadUserCrops()
          this.$toast.success('添加关联成功')
        } else {
          this.$toast.error(res.message || '添加关联失败')
        }
      } catch (e) {
        this.$toast.error('添加关联失败')
      }
    },
    async removeUserCrop(id) {
      try {
        const res = await deleteUserCrop(id)
        if (res.code === 0) {
          this.userCrops = this.userCrops.filter(item => item.id !== id)
          this.$toast.success('删除关联成功')
        } else {
          this.$toast.error(res.message || '删除关联失败')
        }
      } catch (e) {
        this.$toast.error('删除关联失败')
      }
    },
    async editUserCrop(payload) {
      if (!payload || !payload.userId || !payload.cropId) return
      try {
        const res = await updateUserCrop(payload.id, payload.userId, payload.cropId)
        if (res.code === 0) {
          await this.loadUserCrops()
          this.$toast.success('修改关联成功')
        } else {
          this.$toast.error(res.message || '修改关联失败')
        }
      } catch (e) {
        this.$toast.error('修改关联失败')
      }
    },
    now() {
      return new Date().toISOString().slice(0, 19).replace('T', ' ')
    },
    nextTempId() {
      const id = this.tempIdSeed
      this.tempIdSeed -= 1
      return id
    }
  }
}
</script>

