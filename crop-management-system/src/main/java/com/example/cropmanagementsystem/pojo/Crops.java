package com.example.cropmanagementsystem.pojo;

import jakarta.persistence.Id;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 作物表实体类
 * 对应数据库：crops 表
 */
@Data // 自动生成getter/setter/toString等方法（需要引入Lombok依赖）

public class Crops {

    @Id
    private Integer id;
    private String name;

    /**
     * 学名
     * 对应数据库：scientific_name
     */
    private String scientificName;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    //软删除
    private LocalDateTime deletedAt;

}