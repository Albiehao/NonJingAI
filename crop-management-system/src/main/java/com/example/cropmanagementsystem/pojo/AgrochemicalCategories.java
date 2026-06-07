package com.example.cropmanagementsystem.pojo;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 农资分类表实体类
 * 对应数据库：agrochemical_categories 表
 */
@Data
public class AgrochemicalCategories {

    private Integer id;

    /**
     * 分类名称
     */
    private String name;

    /**
     * 父分类ID
     */
    private Long parentId;

    /**
     * 分类描述
     */
    private String description;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

}