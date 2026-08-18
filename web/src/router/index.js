import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import BlankLayout from '@/layouts/BlankLayout.vue'
import { useUserStore } from '@/stores/user'
import { useAgentStore } from '@/stores/agent'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: BlankLayout,
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('../views/HomeView.vue'),
          meta: { keepAlive: true, requiresAuth: false }
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/blog',
      name: 'blog',
      component: BlankLayout,
      meta: { requiresAuth: false },
      children: [
        {
          path: '',
          name: 'BlogList',
          component: () => import('../views/BlogView.vue'),
          meta: { requiresAuth: false }
        },
        {
          path: ':slug',
          name: 'BlogDetail',
          component: () => import('../views/BlogDetailView.vue'),
          meta: { requiresAuth: false }
        }
      ]
    },
    {
      path: '/agent',
      name: 'AgentMain',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'AgentComp',
          component: () => import('../views/AgentView.vue'),
          meta: { keepAlive: true, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/agent/:agent_id',
      name: 'AgentSinglePage',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'AgentSingleComp',
          component: () => import('../views/AgentSingleView.vue'),
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/profile',
      name: 'Profile',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'ProfileComp',
          component: () => import('../views/ProfileView.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        }
      ]
    },
    {
      path: '/devices',
      name: 'Devices',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'DeviceManage',
          component: () => import('../views/DeviceView.vue'),
          meta: { keepAlive: true, requiresAuth: true }
        }
      ]
    },
    {
      path: '/graph',
      name: 'graph',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'GraphComp',
          component: () => import('../views/GraphView.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        }
      ]
    },
    {
      path: '/database',
      name: 'database',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'DatabaseComp',
          component: () => import('../views/DataBaseView.vue'),
          meta: { keepAlive: true, requiresAuth: true, requiresAdmin: true }
        },
        {
          path: ':database_id',
          name: 'DatabaseInfoComp',
          component: () => import('../views/DataBaseInfoView.vue'),
          meta: { keepAlive: false, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'DashboardComp',
          component: () => import('../views/DashboardView.vue'),
          meta: { keepAlive: false, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/settings',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'Settings',
          component: () => import('../views/SettingsView.vue'),
          meta: { keepAlive: false, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/crop-admin',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'CropAdmin',
          component: () => import('../views/CropAdminView.vue'),
          meta: { keepAlive: true, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/crop-dict',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'CropDict',
          component: () => import('../views/CropDictView.vue'),
          meta: { keepAlive: true, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/webhook',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'WebhookAdmin',
          component: () => import('../views/WebhookAdminView.vue'),
          meta: { keepAlive: false, requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/mall',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'MallHome',
          component: () => import('../views/mall/MallHome.vue'),
          meta: { keepAlive: true, requiresAuth: true }
        },
        {
          path: 'cart',
          name: 'MallCart',
          component: () => import('../views/mall/Cart.vue'),
          meta: { keepAlive: true, requiresAuth: true }
        },
        {
          path: 'checkout',
          name: 'MallCheckout',
          component: () => import('../views/mall/Checkout.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        },
        {
          path: 'orders',
          name: 'MallOrders',
          component: () => import('../views/mall/OrderList.vue'),
          meta: { keepAlive: true, requiresAuth: true }
        },
        {
          path: 'orders/:id',
          name: 'MallOrderDetail',
          component: () => import('../views/mall/OrderDetail.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        },
        {
          path: 'payment/:orderId',
          name: 'MallPayment',
          component: () => import('../views/mall/Payment.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        },
        {
          path: 'addresses',
          name: 'MallAddresses',
          component: () => import('../views/mall/AddressManage.vue'),
          meta: { keepAlive: true, requiresAuth: true }
        },
        {
          path: ':id',
          name: 'MallDetail',
          component: () => import('../views/mall/MallDetail.vue'),
          meta: { keepAlive: false, requiresAuth: true }
        }
      ]
    },

    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/EmptyView.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth === true)
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin)

  const userStore = useUserStore()

  if (userStore.token && !userStore.userId) {
    try {
      await userStore.getCurrentUser()
    } catch (error) {
      console.error('获取用户信息失败:', error)
      userStore.logout()
    }
  }

  const isLoggedIn = userStore.isLoggedIn
  const isAdmin = userStore.isAdmin

  if (requiresAuth && !isLoggedIn) {
    sessionStorage.setItem('redirect', to.fullPath)
    next('/login')
    return
  }

  if (requiresAdmin && !isAdmin) {
    try {
      const agentStore = useAgentStore()
      if (!agentStore.isInitialized) {
        await agentStore.initialize()
      }

      const defaultAgent = agentStore.defaultAgent
      if (defaultAgent && defaultAgent.id) {
        next(`/agent/${defaultAgent.id}`)
      } else {
        const agentIds = Object.keys(agentStore.agents)
        if (agentIds.length > 0) {
          next(`/agent/${agentIds[0]}`)
        } else {
          next('/')
        }
      }
    } catch (error) {
      console.error('获取智能体信息失败:', error)
      next('/')
    }
    return
  }

  if (to.path === '/login' && isLoggedIn) {
    next('/')
    return
  }

  next()
})

export default router
