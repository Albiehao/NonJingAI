import axios from 'axios'
import router from '@/router'

const request = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 10000
})

// 请求拦截器：自动携带JWT token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    // 如果是FormData，不要手动设置Content-Type，让浏览器自动设置
    if (config.data instanceof FormData) {
      // 删除可能存在的Content-Type，让浏览器自动设置multipart/form-data和boundary
      delete config.headers['Content-Type']
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：处理401和统一错误
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default request