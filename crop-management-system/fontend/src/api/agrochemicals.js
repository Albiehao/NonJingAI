import request from './request'

// 商品相关API
export function getAllAgrochemicals() {
  return request.get('/agrochemicals/getAll')
}

export function getAgrochemicalById(id) {
  return request.get('/agrochemicals/getById/' + id)
}

export function getAgrochemicalsByCategoryId(categoryId) {
  return request.get('/agrochemicals/getByCategoryId/' + categoryId)
}

export function searchAgrochemicals(keyword) {
  return request.get('/agrochemicals/search', { params: { keyword } })
}

export function addAgrochemical(data) {
  return request.post('/agrochemicals/add', data)
}

export function updateAgrochemical(data) {
  return request.post('/agrochemicals/update', data)
}

export function deleteAgrochemical(id) {
  return request.post('/agrochemicals/deleteById/' + id)
}