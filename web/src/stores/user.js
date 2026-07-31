import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAgentStore } from './agent'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('user_token') || '')
  const userId = ref(null)
  const username = ref('')
  const userIdLogin = ref('')
  const phoneNumber = ref('')
  const email = ref('')
  const avatar = ref('')
  const userRole = ref('')
  const address = ref('')
  const latitude = ref(null)
  const longitude = ref(null)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userRole.value === 'admin' || userRole.value === 'superadmin')
  const isSuperAdmin = computed(() => userRole.value === 'superadmin')

  // 头像 URL 统一转为相对路径（兼容数据库中已存的绝对 URL）
  function normalizeAvatarUrl(url) {
    if (!url) return ''
    try {
      const parsed = new URL(url)
      return parsed.pathname
    } catch {
      return url
    }
  }

  // 动作
  async function login(credentials) {
    try {
      const formData = new FormData()
      // 支持 user_id 或 phone_number 登录
      formData.append('username', credentials.loginId) // 使用 loginId 作为通用登录标识
      formData.append('password', credentials.password)

      const response = await fetch('/api/auth/token', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()

        // 如果是 423 锁定状态码，抛出包含状态码的错误
        if (response.status === 423) {
          const lockError = new Error(error.detail || '账户被锁定')
          lockError.status = 423
          lockError.headers = response.headers
          throw lockError
        }

        throw new Error(error.detail || '登录失败')
      }

      const data = await response.json()

      // 更新状态
      token.value = data.access_token
      userId.value = data.user_id
      username.value = data.username
      userIdLogin.value = data.user_id_login
      phoneNumber.value = data.phone_number || ''
      email.value = data.email || ''
      avatar.value = normalizeAvatarUrl(data.avatar)
      userRole.value = data.role

      // 只保存 token 到本地存储
      localStorage.setItem('user_token', data.access_token)

      return true
    } catch (error) {
      console.error('登录错误:', error)
      throw error
    }
  }

  function logout() {
    // 清除状态
    token.value = ''
    userId.value = null
    username.value = ''
    userIdLogin.value = ''
    phoneNumber.value = ''
    email.value = ''
    avatar.value = ''
    userRole.value = ''
    address.value = ''
    latitude.value = null
    longitude.value = null

    // 清除 agentStore 状态，确保重新登录时能正确加载数据
    const agentStore = useAgentStore()
    agentStore.reset()

    // 只清除 token
    localStorage.removeItem('user_token')
  }

  async function initialize(admin) {
    try {
      const response = await fetch('/api/auth/initialize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(admin)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '初始化管理员失败')
      }

      const data = await response.json()

      // 更新状态
      token.value = data.access_token
      userId.value = data.user_id
      username.value = data.username
      userIdLogin.value = data.user_id_login
      phoneNumber.value = data.phone_number || ''
      email.value = data.email || ''
      avatar.value = normalizeAvatarUrl(data.avatar)
      userRole.value = data.role

      // 只保存 token 到本地存储
      localStorage.setItem('user_token', data.access_token)

      return true
    } catch (error) {
      console.error('初始化管理员错误:', error)
      throw error
    }
  }

  async function checkFirstRun() {
    try {
      const response = await fetch('/api/auth/check-first-run')
      const data = await response.json()
      return data.first_run
    } catch (error) {
      console.error('检查首次运行状态错误:', error)
      return false
    }
  }

  // 用于 API 请求的授权头
  function getAuthHeaders() {
    return {
      Authorization: `Bearer ${token.value}`
    }
  }

  // 用户管理功能
  async function getUsers() {
    try {
      const response = await fetch('/api/auth/users', {
        headers: {
          ...getAuthHeaders()
        }
      })

      if (!response.ok) {
        throw new Error('获取用户列表失败')
      }

      return await response.json()
    } catch (error) {
      console.error('获取用户列表错误:', error)
      throw error
    }
  }

  async function createUser(userData) {
    try {
      const response = await fetch('/api/auth/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(userData)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '创建用户失败')
      }

      return await response.json()
    } catch (error) {
      console.error('创建用户错误:', error)
      throw error
    }
  }

  async function updateUser(userId, userData) {
    try {
      const response = await fetch(`/api/auth/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(userData)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '更新用户失败')
      }

      return await response.json()
    } catch (error) {
      console.error('更新用户错误:', error)
      throw error
    }
  }

  async function deleteUser(userId) {
    try {
      const response = await fetch(`/api/auth/users/${userId}`, {
        method: 'DELETE',
        headers: {
          ...getAuthHeaders()
        }
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '删除用户失败')
      }

      return await response.json()
    } catch (error) {
      console.error('删除用户错误:', error)
      throw error
    }
  }

  // 验证用户名并生成 user_id
  async function validateUsernameAndGenerateUserId(username) {
    try {
      const response = await fetch('/api/auth/validate-username', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify({ username })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '用户名验证失败')
      }

      return await response.json()
    } catch (error) {
      console.error('用户名验证错误:', error)
      throw error
    }
  }

  // 上传头像
  async function uploadAvatar(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/auth/upload-avatar', {
        method: 'POST',
        headers: {
          ...getAuthHeaders()
        },
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '头像上传失败')
      }

      const data = await response.json()

      // 更新本地头像状态
      avatar.value = normalizeAvatarUrl(data.avatar_url)

      return data
    } catch (error) {
      console.error('头像上传错误:', error)
      throw error
    }
  }

  // 获取当前用户信息
  async function getCurrentUser() {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          ...getAuthHeaders()
        }
      })

      if (!response.ok) {
        throw new Error('获取用户信息失败')
      }

      const userData = await response.json()

      // 更新本地状态
      userId.value = userData.id
      username.value = userData.username
      userIdLogin.value = userData.user_id
      phoneNumber.value = userData.phone_number || ''
      email.value = userData.email || ''
      avatar.value = normalizeAvatarUrl(userData.avatar)
      userRole.value = userData.role
      address.value = userData.address || ''
      latitude.value = userData.latitude || null
      longitude.value = userData.longitude || null

      return userData
    } catch (error) {
      console.error('获取用户信息错误:', error)
      throw error
    }
  }

  // 更新个人资料
  async function updateProfile(profileData) {
    try {
      const response = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(profileData)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '更新个人资料失败')
      }

      const userData = await response.json()

      // 更新本地状态
      if (typeof userData.username === 'string') {
        username.value = userData.username
      }
      if (typeof userData.phone_number !== 'undefined') {
        phoneNumber.value = userData.phone_number || ''
      }

      return userData
    } catch (error) {
      console.error('更新个人资料错误:', error)
      throw error
    }
  }

  return {
    // 状态
    token,
    userId,
    username,
    userIdLogin,
    phoneNumber,
    email,
    avatar,
    userRole,
    address,
    latitude,
    longitude,

    // 计算属性
    isLoggedIn,
    isAdmin,
    isSuperAdmin,

    // 方法
    login,
    logout,
    initialize,
    checkFirstRun,
    getAuthHeaders,
    getUsers,
    createUser,
    updateUser,
    deleteUser,
    validateUsernameAndGenerateUserId,
    uploadAvatar,
    getCurrentUser,
    updateProfile
  }
})

// 检查当前用户是否有管理员权限
export const checkAdminPermission = () => {
  const userStore = useUserStore()
  if (!userStore.isAdmin) {
    throw new Error('需要管理员权限')
  }
  return true
}

// 检查当前用户是否有超级管理员权限
export const checkSuperAdminPermission = () => {
  const userStore = useUserStore()
  return userStore.isSuperAdmin
}
