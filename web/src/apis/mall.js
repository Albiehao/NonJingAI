import { useUserStore } from '@/stores/user'
import { mockCategories, mockProductList, mockProductDetails } from './mockData'

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
    const data = await res.json()
    // 如果后端返回空数据，使用 mock 数据
    if (data.code === 0 && (!data.data || data.data.length === 0)) {
        return { code: 0, data: mockCategories }
    }
    return data
}

export async function getAllProducts() {
    const res = await fetch('/crop-api/agrochemicals/getAll', { headers: getHeaders() })
    if (!res.ok) throw new Error('加载商品失败')
    const data = await res.json()
    // 如果后端返回空数据，使用 mock 列表数据（简化版）
    if (data.code === 0 && (!data.data || data.data.length === 0)) {
        return { code: 0, data: mockProductList }
    }
    return data
}

export async function getProductsByCategoryId(categoryId) {
    const res = await fetch(`/crop-api/agrochemicals/getByCategoryId/${categoryId}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('加载商品失败')
    const data = await res.json()
    // 如果后端返回空数据，使用 mock 列表数据按分类筛选
    if (data.code === 0 && (!data.data || data.data.length === 0)) {
        const filtered = mockProductList.filter(p => p.id === Number(categoryId))
        return { code: 0, data: filtered }
    }
    return data
}

export async function searchProducts(keyword) {
    const res = await fetch(`/crop-api/agrochemicals/search?keyword=${encodeURIComponent(keyword)}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('搜索商品失败')
    const data = await res.json()
    // 如果后端返回空数据，使用 mock 列表数据按关键词筛选
    if (data.code === 0 && (!data.data || data.data.length === 0)) {
        const kw = keyword.toLowerCase()
        const filtered = mockProductList.filter(p =>
            p.productName.toLowerCase().includes(kw) ||
            p.brand.toLowerCase().includes(kw)
        )
        return { code: 0, data: filtered }
    }
    return data
}

export async function getProductById(id) {
    const res = await fetch(`/crop-api/agrochemicals/getById/${id}`, {
        headers: getHeaders()
    })
    if (!res.ok) throw new Error('加载商品详情失败')
    const data = await res.json()
    // 如果后端返回空数据，使用 mock 详情数据（完整版）
    if (data.code === 0 && !data.data) {
        const product = mockProductDetails.find(p => p.id === Number(id))
        return { code: 0, data: product || null }
    }
    return data
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