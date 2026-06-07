import { apiGet, apiPost } from './base'

/**
 * 邮箱绑定 API
 */

export async function sendEmailCode(email) {
  return apiPost('/api/email/binding/send-code', { email })
}

export async function verifyEmailCode(email, code) {
  return apiPost('/api/email/binding/verify', { email, code })
}

export async function getEmailBindingStatus() {
  return apiGet('/api/email/binding/status')
}

export async function unbindEmail() {
  return apiPost('/api/email/binding/unbind')
}
