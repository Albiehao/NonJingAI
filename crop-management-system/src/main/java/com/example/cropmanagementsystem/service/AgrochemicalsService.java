package com.example.cropmanagementsystem.service;

import com.example.cropmanagementsystem.pojo.Agrochemicals;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface AgrochemicalsService {

    /**
     * 添加商品
     */
    void add(Agrochemicals agrochemicals);

    /**
     * 修改商品
     */
    void update(Agrochemicals agrochemicals);

    /**
     * 软删除商品
     */
    void deleteById(Long id);

    /**
     * 根据ID获取商品
     */
    Agrochemicals getById(Long id);

    /**
     * 获取所有商品
     */
    List<Agrochemicals> getAll();

    /**
     * 根据分类ID获取商品列表
     */
    List<Agrochemicals> getByCategoryId(Integer categoryId);

    /**
     * 搜索商品
     */
    List<Agrochemicals> search(String keyword);

}