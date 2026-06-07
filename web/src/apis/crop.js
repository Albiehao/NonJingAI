/**
 * 农资管理 API 模块 - 通过 /crop-api 代理调用 Java 后端
 */

const CROP_API_PREFIX = '/crop-api'

function getToken() {
  return localStorage.getItem('crop_token')
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(url, options = {}) {
  const headers = { ...authHeaders(), ...options.headers }
  const response = await fetch(`${CROP_API_PREFIX}${url}`, { ...options, headers })
  return response.json()
}

/** 构建表单数据 */
function toFormData(params) {
  const fd = new FormData()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null) fd.append(k, String(v))
  })
  return fd
}

// ===== 用户认证 =====

export function cropLogin(username, password) {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  return request('/user/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params
  })
}

export function cropGetUser(id) {
  return request(`/user/get/${id}`, { method: 'POST' })
}

// ===== 分类管理 =====

export function getCategories() {
  return request('/categories/getAll')
}

export function getTopCategories() {
  return request('/categories/getTopCategories')
}

export function getSubCategories(parentId) {
  return request(`/categories/getByParentId/${parentId}`)
}

export function getCategoryById(id) {
  return request(`/categories/getById/${id}`)
}

export function addCategory(name, parentId, description) {
  return request('/categories/add', {
    method: 'POST',
    body: toFormData({ name, parentId, description })
  })
}

export function updateCategory(id, name, parentId, description) {
  return request(`/categories/update/${id}`, {
    method: 'POST',
    body: toFormData({ name, parentId, description })
  })
}

export function deleteCategory(id) {
  return request(`/categories/deleteById/${id}`, { method: 'POST' })
}

// ===== 农资管理 =====

export function getAgrochemicals() {
  return request('/agrochemicals/getAll')
}

export function getAgrochemicalById(id) {
  return request(`/agrochemicals/getById/${id}`)
}

export function getAgrochemicalsByCategory(categoryId) {
  return request(`/agrochemicals/getByCategoryId/${categoryId}`)
}

export function searchAgrochemicals(keyword) {
  return request(`/agrochemicals/search?keyword=${encodeURIComponent(keyword)}`)
}

export function addAgrochemical(data) {
  return request('/agrochemicals/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}

export function updateAgrochemical(data) {
  return request('/agrochemicals/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}

export function deleteAgrochemical(id) {
  return request(`/agrochemicals/deleteById/${id}`, { method: 'POST' })
}

// ===== 作物管理 =====

export function getCrops() {
  return request('/crops/getAll', { method: 'POST' })
}

export function getCropById(id) {
  return request(`/crops/getById/${id}`, { method: 'POST' })
}

export function addCrop(name, scientificName) {
  return request('/crops/add', {
    method: 'POST',
    body: toFormData({ name, scientificName })
  })
}

export function updateCrop(id, name, scientificName) {
  return request(`/crops/update/${id}`, {
    method: 'POST',
    body: toFormData({ name, scientificName })
  })
}

export function deleteCrop(id) {
  return request(`/crops/deleteById/${id}`, { method: 'POST' })
}

// ===== 文件上传 =====

export function uploadFile(file, bucket = 'crop-images') {
  const fd = new FormData()
  fd.append('file', file)
  fd.append('bucket', bucket)
  return fetch(`${CROP_API_PREFIX}/file/upload`, {
    method: 'POST',
    body: fd
  }).then((r) => r.json())
}

// ===== Token 管理 =====

export function getCropToken() {
  return getToken()
}

export function setCropToken(token) {
  localStorage.setItem('crop_token', token)
}

export function setCropUser(user) {
  localStorage.setItem('crop_user', JSON.stringify(user))
}

export function getCropUser() {
  try {
    return JSON.parse(localStorage.getItem('crop_user'))
  } catch {
    return null
  }
}

export function clearCropAuth() {
  localStorage.removeItem('crop_token')
  localStorage.removeItem('crop_user')
}

export function isCropLoggedIn() {
  return !!getToken()
}
