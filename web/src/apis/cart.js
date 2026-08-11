import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { mockCartItems } from '@/apis/mockData'

const STORAGE_KEY = 'cart_items'

export const useCartStore = defineStore('cart', () => {
    const items = ref([])
    let initialized = false

    function _persist() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
    }

    function _load() {
        if (initialized) return
        initialized = true
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
            try {
                items.value = JSON.parse(saved)
            } catch {
                items.value = JSON.parse(JSON.stringify(mockCartItems))
            }
        } else {
            items.value = JSON.parse(JSON.stringify(mockCartItems))
        }
    }

    const cartCount = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))

    function addToCart(productId, quantity = 1, productInfo) {
        _load()
        const existing = items.value.find((i) => i.productId === productId)
        if (existing) {
            existing.quantity += quantity
        } else {
            const maxId = items.value.reduce((max, i) => Math.max(max, i.id), 0)
            items.value.push({
                id: maxId + 1,
                productId,
                productName: productInfo?.productName || '',
                mainImage: productInfo?.mainImage || '',
                price: productInfo?.price || 0,
                quantity
            })
        }
        _persist()
    }

    function updateQuantity(id, quantity) {
        const item = items.value.find((i) => i.id === id)
        if (item) {
            item.quantity = Math.max(1, Math.min(99, quantity))
            _persist()
        }
    }

    function removeItem(id) {
        items.value = items.value.filter((i) => i.id !== id)
        _persist()
    }

    function clearCart() {
        items.value = []
        _persist()
    }

    return { items, cartCount, addToCart, updateQuantity, removeItem, clearCart }
})