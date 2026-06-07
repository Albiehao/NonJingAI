package com.example.cropmanagementsystem.pojo;

import jakarta.persistence.Id;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 用户-农作物关联表实体类
 * 对应数据库：user_crops 表
 */
@Data
public class UserCrops {

    @Id
    private Integer id;

    /**
     * 用户ID
     * 对应数据库：user_id
     */
    private Integer userId;

    /**
     * 农作物ID
     * 对应数据库：crop_id
     */
    private Integer cropId;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    /**
     * 软删除时间
     */
    private LocalDateTime deletedAt;

}