import { apiAdminGet, apiAdminPost, apiAdminPut, apiAdminDelete } from './base'

/**
 * Webhook 推送管理 API 模块
 */

export const webhookApi = {
  /**
   * 获取所有 Webhook 源配置
   */
  listSources: async () => apiAdminGet('/api/webhook/sources'),

  /**
   * 获取单个 Webhook 源
   */
  getSource: async (sourceId) => apiAdminGet(`/api/webhook/sources/${sourceId}`),

  /**
   * 创建 Webhook 源
   */
  createSource: async (data) => apiAdminPost('/api/webhook/sources', data),

  /**
   * 更新 Webhook 源
   */
  updateSource: async (sourceId, data) => apiAdminPut(`/api/webhook/sources/${sourceId}`, data),

  /**
   * 删除 Webhook 源
   */
  deleteSource: async (sourceId) => apiAdminDelete(`/api/webhook/sources/${sourceId}`),

  /**
   * 测试 Webhook 源（预览渲染效果）
   */
  testSource: async (sourceId, mockBody) =>
    apiAdminPost(`/api/webhook/sources/${sourceId}/test`, { mock_body: mockBody }),

  /**
   * 获取 Webhook 事件记录
   */
  listEvents: async (params = {}) => {
    const query = new URLSearchParams()
    if (params.source_id) query.set('source_id', params.source_id)
    if (params.skip) query.set('skip', params.skip)
    if (params.limit) query.set('limit', params.limit)
    const qs = query.toString()
    return apiAdminGet(`/api/webhook/events${qs ? '?' + qs : ''}`)
  },

  /**
   * 获取 Webhook 事件详情
   */
  getEvent: async (eventId) => apiAdminGet(`/api/webhook/events/${eventId}`),

  /**
   * 内部快速推送
   */
  quickPush: async (data) => apiAdminPost('/api/webhook/quick-push', data),
}
