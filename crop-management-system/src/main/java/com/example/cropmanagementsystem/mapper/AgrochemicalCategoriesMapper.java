package com.example.cropmanagementsystem.mapper;

import com.example.cropmanagementsystem.pojo.AgrochemicalCategories;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface AgrochemicalCategoriesMapper {

    /**
     * 获取所有分类
     */
    @Select("select * from crop_agrochemical_categories")
    List<AgrochemicalCategories> listAll();

    /**
     * 根据ID获取分类
     */
    @Select("select * from crop_agrochemical_categories where id = #{id}")
    AgrochemicalCategories getById(Integer id);

    /**
     * 获取顶级分类（parent_id为NULL）
     */
    @Select("select * from crop_agrochemical_categories where parent_id is null")
    List<AgrochemicalCategories> listTopCategories();

    /**
     * 根据父分类ID获取子分类
     */
    @Select("select * from crop_agrochemical_categories where parent_id = #{parentId}")
    List<AgrochemicalCategories> listByParentId(Long parentId);

    @Insert("insert into crop_agrochemical_categories(name, parent_id, description, created_at, updated_at) " +
            "values(#{name}, #{parentId}, #{description}, NOW(), NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    void add(AgrochemicalCategories category);

    @Update("update crop_agrochemical_categories set name=#{name}, parent_id=#{parentId}, " +
            "description=#{description}, updated_at=NOW() where id=#{id}")
    void update(AgrochemicalCategories category);

    @Delete("delete from crop_agrochemical_categories where id = #{id}")
    void deleteById(Integer id);
}