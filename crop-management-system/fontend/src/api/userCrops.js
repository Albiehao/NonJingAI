import request from './request'

// 用户-作物关联API
export function addUserCrop(userId, cropId) {
  const params = new URLSearchParams()
  params.append('userId', userId)
  params.append('cropId', cropId)
  return request.post('/userCrops/add', params)
}

export function updateUserCrop(id, userId, cropId) {
  const params = new URLSearchParams()
  params.append('userId', userId)
  params.append('cropId', cropId)
  return request.post('/userCrops/update/' + id, params)
}

export function deleteUserCrop(id) {
  return request.post('/userCrops/delete/' + id)
}

export function getUserCropsByUserId(userId) {
  return request.post('/userCrops/getByUser/' + userId)
}

export function getUserCropsByCropId(cropId) {
  return request.post('/userCrops/getByCrop/' + cropId)
}

export function getAllUserCrops() {
  return request.post('/userCrops/getAll')
}