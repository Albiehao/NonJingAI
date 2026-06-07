import request from './request'

// 分类相关API
export function getAllCategories() {
  return request.get('/categories/getAll')
}

export function getCategoryById(id) {
  return request.get('/categories/getById/' + id)
}

export function getTopCategories() {
  return request.get('/categories/getTopCategories')
}

export function getCategoriesByParentId(parentId) {
  return request.get('/categories/getByParentId/' + parentId)
}