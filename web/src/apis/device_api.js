import { apiDelete, apiGet, apiPost } from './base'

export function getBoundDevices() {
  return apiGet('/api/devices')
}

export function bindDevice(sn, password) {
  return apiPost('/api/devices/bind', { sn, password })
}

export function unbindDevice(sn) {
  return apiDelete(`/api/devices/${encodeURIComponent(sn)}`)
}
