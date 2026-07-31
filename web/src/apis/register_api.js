import { apiPost, apiGet } from './base'

export async function sendRegisterCode(email) {
  return apiPost('/api/auth/register/send-code', { email }, {}, false)
}

export async function registerUser(data) {
  return apiPost('/api/auth/register', data, {}, false)
}
