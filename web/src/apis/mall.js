import { useUserStore } from '@/stores/user'

function getHeaders(requiresAuth = true) {
    const headers = { 'Content-Type': 'application/json' }
    if (requiresAuth) {
        const userStore = useUserStore()
        if (userStore.isLoggedIn) {
            Object.assign(headers, userStore.getAuthHeaders())
        }
    }
    return headers
}

export async function getCategories() {
    const res = await fetch('/crop-api/categories/getAll', { headers: getHeaders() })
    if (!res.ok) throw new Error('加载分类失败')
    return res.json()
}

export async function getAllProducts() {
    const res = await fetch('/crop-api/agrochemicals/getAll', { headers: getHeaders() })
    if (!res.ok) throw new Error('加载商品失败')
    return res.json()
}

export async function getProductsByCategoryId(categoryId) {
    const res = await fetch(`/crop-api/agrochemicals/getByCategoryId/${categoryId}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('加载商品失败')
    return res.json()
}

export async function searchProducts(keyword) {
    const res = await fetch(`/crop-api/agrochemicals/search?keyword=${encodeURIComponent(keyword)}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('搜索商品失败')
    return res.json()
}
export async function getProductById(id) {
    const res = await fetch(`/crop-api/agrochemicals/getById/${id}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('加载商品详情失败')
    return res.json()
}
export async function addToCart(productId, quantity = 1) {
    const res = await fetch('/crop-api/cart/add', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ product_id: productId, quantity })
    })
    if (!res.ok) {
        if (res.status === 401) throw new Error('请先登录')
        throw new Error('加入购物车失败')
    }
    return res.json()
}
