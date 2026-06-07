import request from './request'

// 后端crops接口使用表单参数
export function addCrop(name, scientificName) {
  const params = new URLSearchParams()
  params.append('name', name)
  params.append('scientificName', scientificName)
  return request.post('/crops/add', params)
}

export function updateCrop(id, name, scientificName) {
  const params = new URLSearchParams()
  params.append('name', name)
  params.append('scientificName', scientificName)
  return request.post('/crops/update/' + id, params)
}

export function deleteCrop(id) {
  return request.post('/crops/deleteById/' + id)
}

export function getCropById(id) {
  return request.post('/crops/getById/' + id)
}

export function getAllCrops() {
  return request.post('/crops/getAll')
}
