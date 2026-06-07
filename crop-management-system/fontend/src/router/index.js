import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import BrandStoryView from '../views/BrandStoryView.vue'
import AdminShell from '../pages/admin/AdminShell.vue'
import UserCenterView from '../views/UserCenterView.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/products', name: 'products', component: ProductsView },
  { path: '/products/:id', name: 'product-detail', component: ProductDetailView },
  { path: '/story', name: 'story', component: BrandStoryView },
  {
    path: '/user-center',
    name: 'user-center',
    component: UserCenterView,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (!token) {
        window.$toast.warning('请先登录')
        setTimeout(() => next('/login'), 500)
      } else {
        next()
      }
    }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminShell,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      const role = localStorage.getItem('role')
      if (!token) {
        window.$toast.warning('请先登录')
        setTimeout(() => next('/login'), 500)
      } else if (role !== 'ADMIN') {
        window.$toast.error('权限不足，只有管理员可以访问')
        setTimeout(() => next('/'), 500)
      } else {
        next()
      }
    }
  },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

// 捕获重复导航错误
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => {
    if (err.name === 'NavigationDuplicated') return
    throw err
  })
}

export default router
