import {
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  apiAdminGet,
  apiAdminPost,
  apiAdminPut,
  apiAdminDelete
} from './base'

// =============================================================================
// 农作物字典 CRUD（管理员）
// =============================================================================

export function listCrops(category) {
  const params = category ? `?category=${category}` : ''
  return apiGet(`/api/crops${params}`, {}, true)
}

export function createCrop(data) {
  return apiAdminPost('/api/crops', data)
}

export function updateCrop(id, data) {
  return apiAdminPut(`/api/crops/${id}`, data)
}

export function deleteCrop(id) {
  return apiAdminDelete(`/api/crops/${id}`)
}

// =============================================================================
// 用户农作物关联
// =============================================================================

export function listMyCrops() {
  return apiGet('/api/crops/my', {}, true)
}

export function addMyCrop(data) {
  return apiPost('/api/crops/my', data, {}, true)
}

export function removeMyCrop(id) {
  return apiDelete(`/api/crops/my/${id}`, {}, true)
}

// =============================================================================
// 用户地址管理
// =============================================================================

export function updateAddress(data) {
  return apiPut('/api/crops/address', data, {}, true)
}
