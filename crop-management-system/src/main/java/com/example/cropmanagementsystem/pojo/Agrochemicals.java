package com.example.cropmanagementsystem.pojo;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 农资商品信息表实体类
 * 对应数据库：agrochemicals 表
 */
@Data
public class Agrochemicals {

    private Long id;

    /**
     * 分类ID
     */
    private Integer categoryId;

    /**
     * 商品编号 (如: sp-002)
     */
    private String productCode;

    /**
     * 商品全称/商品名
     */
    private String productName;

    /**
     * 品牌/生产厂家
     */
    private String brand;

    /**
     * 月销量
     */
    private Integer monthlySales;

    /**
     * 价格
     */
    private BigDecimal price;

    /**
     * 农药登记证号
     */
    private String registrationNo;

    /**
     * 剂型代码/名称
     */
    private String formulation;

    /**
     * 含量规格
     */
    private String contentSpec;

    /**
     * 产品展示图 URL
     */
    private String mainImage;

    /**
     * 商品描述
     */
    private String description;

    /**
     * 适用农作物
     */
    private String useCrops;

    /**
     * 用法说明
     */
    private String usageMethod;

    /**
     * 注意事项
     */
    private String precautions;

    /**
     * 多平台购买链接
     */
    private String purchaseLinks;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    /**
     * 软删除时间戳
     */
    private LocalDateTime deletedAt;

}