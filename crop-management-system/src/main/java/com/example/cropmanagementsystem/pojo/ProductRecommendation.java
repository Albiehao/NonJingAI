package com.example.cropmanagementsystem.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 产品推荐 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProductRecommendation {

    /**
     * 产品ID
     */
    private Long productId;

    /**
     * 产品名称
     */
    private String productName;

    /**
     * 跳转URL
     */
    private String jumpUrl;

    /**
     * 产品图片
     */
    private String mainImage;

    /**
     * 价格
     */
    private String price;

}