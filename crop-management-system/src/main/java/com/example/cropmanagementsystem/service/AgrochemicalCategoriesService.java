package com.example.cropmanagementsystem.service;

import com.example.cropmanagementsystem.pojo.AgrochemicalCategories;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface AgrochemicalCategoriesService {

    /**
     * 获取所有分类
     */
    List<AgrochemicalCategories> getAll();

    /**
     * 根据ID获取分类
     */
    AgrochemicalCategories getById(Integer id);

    /**
     * 获取顶级分类
     */
    List<AgrochemicalCategories> getTopCategories();

    /**
     * 根据父分类ID获取子分类
     */
    List<AgrochemicalCategories> getByParentId(Long parentId);

    void add(AgrochemicalCategories category);

    void update(AgrochemicalCategories category);

    void deleteById(Integer id);
}