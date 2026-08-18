// Mock 分类数据
export const mockCategories = [
    { id: 1, name: '杀菌剂', parentId: null },
    { id: 2, name: '杀虫剂', parentId: null },
    { id: 3, name: '除草剂', parentId: null },
    { id: 4, name: '肥料', parentId: null }
]

// Mock 商品列表数据（简化版 - 用于 MallHome.vue）
// 只包含：id, productName, brand, price, mainImage, monthlySales, useCrops
export const mockProductList = [
    {
        id: 1,
        productName: '多菌灵可湿性粉剂',
        brand: '绿丰农化',
        price: 49.90,
        mainImage: 'https://picsum.photos/seed/product1/400/400',
        monthlySales: 156,
        useCrops: '水稻、小麦、玉米'
    },
    {
        id: 2,
        productName: '吡虫啉乳油',
        brand: '农达化工',
        price: 35.50,
        mainImage: 'https://picsum.photos/seed/product2/400/400',
        monthlySales: 234,
        useCrops: '水稻、棉花、蔬菜'
    },
    {
        id: 3,
        productName: '草甘膦异丙胺盐水剂',
        brand: '丰收植保',
        price: 28.00,
        mainImage: 'https://picsum.photos/seed/product3/400/400',
        monthlySales: 412,
        useCrops: '非耕地、果园'
    },
    {
        id: 4,
        productName: '复合肥（15-15-15）',
        brand: '金土地肥料',
        price: 120.00,
        mainImage: 'https://picsum.photos/seed/product4/400/400',
        monthlySales: 89,
        useCrops: '水稻、小麦、玉米、果树'
    },
    {
        id: 5,
        productName: '代森锰锌可湿性粉剂',
        brand: '绿丰农化',
        price: 42.00,
        mainImage: 'https://picsum.photos/seed/product5/400/400',
        monthlySales: 178,
        useCrops: '番茄、黄瓜、马铃薯'
    },
    {
        id: 6,
        productName: '高效氯氟氰菊酯乳油',
        brand: '农达化工',
        price: 55.80,
        mainImage: 'https://picsum.photos/seed/product6/400/400',
        monthlySales: 267,
        useCrops: '棉花、蔬菜、果树'
    },
    {
        id: 7,
        productName: '2,4-D丁酯乳油',
        brand: '丰收植保',
        price: 18.50,
        mainImage: 'https://picsum.photos/seed/product7/400/400',
        monthlySales: 145,
        useCrops: '小麦'
    },
    {
        id: 8,
        productName: '尿素（含缩二脲≤1%）',
        brand: '金土地肥料',
        price: 95.00,
        mainImage: 'https://picsum.photos/seed/product8/400/400',
        monthlySales: 523,
        useCrops: '水稻、小麦、玉米、蔬菜'
    },
    {
        id: 9,
        productName: '甲基托布津可湿性粉剂',
        brand: '绿丰农化',
        price: 38.00,
        mainImage: 'https://picsum.photos/seed/product9/400/400',
        monthlySales: 198,
        useCrops: '草莓、葡萄、花卉'
    },
    {
        id: 10,
        productName: '阿维菌素乳油',
        brand: '农达化工',
        price: 68.00,
        mainImage: 'https://picsum.photos/seed/product10/400/400',
        monthlySales: 312,
        useCrops: '柑橘、苹果、蔬菜'
    }
]

// Mock 商品详情数据（完整版 - 用于 MallDetail.vue）
// 包含全部字段：id, productName, brand, price, mainImage, monthlySales, registrationNo, formulation, contentSpec, description, useCrops, usageMethod, precautions, purchaseLinks
export const mockProductDetails = [
    {
        id: 1,
        productName: '多菌灵可湿性粉剂',
        brand: '绿丰农化',
        price: 49.90,
        mainImage: 'https://picsum.photos/seed/product1/400/400',
        monthlySales: 156,
        registrationNo: 'PD20200001',
        formulation: '可湿性粉剂',
        contentSpec: '500g/袋',
        description: '高效广谱杀菌剂，对多种作物病害有良好防治效果',
        useCrops: '水稻、小麦、玉米',
        usageMethod: '稀释800-1000倍喷雾',
        precautions: '避免与碱性农药混用，施药时穿戴防护服',
        purchaseLinks: 'https://example.com/product1'
    },
    {
        id: 2,
        productName: '吡虫啉乳油',
        brand: '农达化工',
        price: 35.50,
        mainImage: 'https://picsum.photos/seed/product2/400/400',
        monthlySales: 234,
        registrationNo: 'PD20190002',
        formulation: '乳油',
        contentSpec: '200ml/瓶',
        description: '高效低毒杀虫剂，对蚜虫、飞虱等刺吸式口器害虫特效',
        useCrops: '水稻、棉花、蔬菜',
        usageMethod: '稀释1500-2000倍喷雾',
        precautions: '对蜜蜂有毒，花期禁用',
        purchaseLinks: 'https://example.com/product2'
    },
    {
        id: 3,
        productName: '草甘膦异丙胺盐水剂',
        brand: '丰收植保',
        price: 28.00,
        mainImage: 'https://picsum.photos/seed/product3/400/400',
        monthlySales: 412,
        registrationNo: 'PD20180003',
        formulation: '水剂',
        contentSpec: '1L/瓶',
        description: '灭生性除草剂，用于非耕地除草',
        useCrops: '非耕地、果园',
        usageMethod: '稀释100-200倍定向喷雾',
        precautions: '避免飘移到作物上，施药后7天内勿放牧',
        purchaseLinks: 'https://example.com/product3'
    },
    {
        id: 4,
        productName: '复合肥（15-15-15）',
        brand: '金土地肥料',
        price: 120.00,
        mainImage: 'https://picsum.photos/seed/product4/400/400',
        monthlySales: 89,
        registrationNo: '肥料登记证20210004',
        formulation: '颗粒',
        contentSpec: '50kg/袋',
        description: '氮磷钾均衡复合肥，适用于多种作物基肥和追肥',
        useCrops: '水稻、小麦、玉米、果树',
        usageMethod: '基肥每亩施用30-50kg',
        precautions: '避免与种子直接接触，存放于干燥处',
        purchaseLinks: 'https://example.com/product4'
    },
    {
        id: 5,
        productName: '代森锰锌可湿性粉剂',
        brand: '绿丰农化',
        price: 42.00,
        mainImage: 'https://picsum.photos/seed/product5/400/400',
        monthlySales: 178,
        registrationNo: 'PD20200005',
        formulation: '可湿性粉剂',
        contentSpec: '400g/袋',
        description: '保护性杀菌剂，预防多种真菌性病害',
        useCrops: '番茄、黄瓜、马铃薯',
        usageMethod: '稀释600-800倍喷雾',
        precautions: '不能与铜制剂混用',
        purchaseLinks: 'https://example.com/product5'
    },
    {
        id: 6,
        productName: '高效氯氟氰菊酯乳油',
        brand: '农达化工',
        price: 55.80,
        mainImage: 'https://picsum.photos/seed/product6/400/400',
        monthlySales: 267,
        registrationNo: 'PD20190006',
        formulation: '乳油',
        contentSpec: '100ml/瓶',
        description: '广谱杀虫剂，对鳞翅目、鞘翅目害虫有效',
        useCrops: '棉花、蔬菜、果树',
        usageMethod: '稀释2000-3000倍喷雾',
        precautions: '对鱼类高毒，远离水产养殖区',
        purchaseLinks: 'https://example.com/product6'
    },
    {
        id: 7,
        productName: '2,4-D丁酯乳油',
        brand: '丰收植保',
        price: 18.50,
        mainImage: 'https://picsum.photos/seed/product7/400/400',
        monthlySales: 145,
        registrationNo: 'PD20170007',
        formulation: '乳油',
        contentSpec: '500ml/瓶',
        description: '选择性除草剂，用于小麦田防除阔叶杂草',
        useCrops: '小麦',
        usageMethod: '每亩用量50-80ml，兑水30kg喷雾',
        precautions: '对阔叶作物敏感，避免飘移',
        purchaseLinks: 'https://example.com/product7'
    },
    {
        id: 8,
        productName: '尿素（含缩二脲≤1%）',
        brand: '金土地肥料',
        price: 95.00,
        mainImage: 'https://picsum.photos/seed/product8/400/400',
        monthlySales: 523,
        registrationNo: '肥料登记证20200008',
        formulation: '颗粒',
        contentSpec: '50kg/袋',
        description: '高氮肥料，促进作物茎叶生长',
        useCrops: '水稻、小麦、玉米、蔬菜',
        usageMethod: '追肥每亩施用10-20kg',
        precautions: '避免与碱性物质混用，存放于阴凉干燥处',
        purchaseLinks: 'https://example.com/product8'
    },
    {
        id: 9,
        productName: '甲基托布津可湿性粉剂',
        brand: '绿丰农化',
        price: 38.00,
        mainImage: 'https://picsum.photos/seed/product9/400/400',
        monthlySales: 198,
        registrationNo: 'PD20210009',
        formulation: '可湿性粉剂',
        contentSpec: '500g/袋',
        description: '内吸性杀菌剂，对灰霉病、白粉病特效',
        useCrops: '草莓、葡萄、花卉',
        usageMethod: '稀释1000-1500倍喷雾',
        precautions: '安全间隔期14天',
        purchaseLinks: 'https://example.com/product9'
    },
    {
        id: 10,
        productName: '阿维菌素乳油',
        brand: '农达化工',
        price: 68.00,
        mainImage: 'https://picsum.photos/seed/product10/400/400',
        monthlySales: 312,
        registrationNo: 'PD20200010',
        formulation: '乳油',
        contentSpec: '100ml/瓶',
        description: '生物源杀虫杀螨剂，对红蜘蛛、潜叶蛾有效',
        useCrops: '柑橘、苹果、蔬菜',
        usageMethod: '稀释3000-5000倍喷雾',
        precautions: '对蚕高毒，桑园附近禁用',
        purchaseLinks: 'https://example.com/product10'
    }
]


export const mockCartItems = [
    {
        id: 1,
        productId: 1,
        productName: '多菌灵可湿性粉剂',
        mainImage: 'https://picsum.photos/seed/product1/400/400',
        price: 49.90,
        quantity: 2
    },
    {
        id: 2,
        productId: 2,
        productName: '吡虫啉乳油',
        mainImage: 'https://picsum.photos/seed/product2/400/400',
        price: 35.50,
        quantity: 1
    },
    {
        id: 3,
        productId: 3,
        productName: '草甘膦异丙胺盐水剂',
        mainImage: 'https://picsum.photos/seed/product3/400/400',
        price: 28.00,
        quantity: 3
    },
    {
        id: 4,
        productId: 4,
        productName: '复合肥（15-15-15）',
        mainImage: 'https://picsum.photos/seed/product4/400/400',
        price: 120.00,
        quantity: 1
    },
    {
        id: 5,
        productId: 5,
        productName: '代森锰锌可湿性粉剂',
        mainImage: 'https://picsum.photos/seed/product5/400/400',
        price: 42.00,
        quantity: 2
    },
    {
        id: 6,
        productId: 6,
        productName: '高效氯氟氰菊酯乳油',
        mainImage: 'https://picsum.photos/seed/product6/400/400',
        price: 55.80,
        quantity: 1
    },
    {
        id: 7,
        productId: 7,
        productName: '2,4-D丁酯乳油',
        mainImage: 'https://picsum.photos/seed/product7/400/400',
        price: 18.50,
        quantity: 4
    },
    {
        id: 8,
        productId: 8,
        productName: '尿素（含缩二脲≤1%）',
        mainImage: 'https://picsum.photos/seed/product8/400/400',
        price: 95.00,
        quantity: 2
    },
    {
        id: 9,
        productId: 9,
        productName: '甲基托布津可湿性粉剂',
        mainImage: 'https://picsum.photos/seed/product9/400/400',
        price: 38.00,
        quantity: 1
    },
    {
        id: 10,
        productId: 10,
        productName: '阿维菌素乳油',
        mainImage: 'https://picsum.photos/seed/product10/400/400',
        price: 68.00,
        quantity: 2
    }
]