import request from './request'

// 后端接口使用表单参数（非JSON body），需要用URLSearchParams发送
export function login(username, password) {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  return request.post('/user/login', params)
}

export function register(username, password, phoneNumber) {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  if (phoneNumber) params.append('phoneNumber', phoneNumber)
  return request.post('/user/register', params)
}

export function getAllUsers() {
  return request.post('/user/getAll')
}

export function getUserById(id) {
  return request.post('/user/get/' + id)
}

export function updateUser(id, data) {
  const formData = new FormData()
  if (data.username) formData.append('username', data.username)
  if (data.phoneNumber) formData.append('phoneNumber', data.phoneNumber)
  if (data.avatar) formData.append('avatar', data.avatar)
  return request.post('/user/update/' + id, formData)
}

export function deleteUser(id) {
  return request.post('/user/delete/' + id)
}
