import { apiGet, apiPost } from './base'

/**
 * 微信公众号绑定 API
 */

export async function generateWeChatBindingToken() {
  return apiGet('/api/wechat/binding/token')
}

export async function getWeChatBindingStatus() {
  return apiGet('/api/wechat/binding/status')
}

export async function unbindWeChat() {
  return apiPost('/api/wechat/binding/unbind')
}
