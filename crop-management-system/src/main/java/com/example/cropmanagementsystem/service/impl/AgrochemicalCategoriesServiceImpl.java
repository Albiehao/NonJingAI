package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.mapper.AgrochemicalCategoriesMapper;
import com.example.cropmanagementsystem.pojo.AgrochemicalCategories;
import com.example.cropmanagementsystem.service.AgrochemicalCategoriesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AgrochemicalCategoriesServiceImpl implements AgrochemicalCategoriesService {

    @Autowired
    private AgrochemicalCategoriesMapper agrochemicalCategoriesMapper;

    @Override
    public List<AgrochemicalCategories> getAll() {
        return agrochemicalCategoriesMapper.listAll();
    }

    @Override
    public AgrochemicalCategories getById(Integer id) {
        return agrochemicalCategoriesMapper.getById(id);
    }

    @Override
    public List<AgrochemicalCategories> getTopCategories() {
        return agrochemicalCategoriesMapper.listTopCategories();
    }

    @Override
    public List<AgrochemicalCategories> getByParentId(Long parentId) {
        return agrochemicalCategoriesMapper.listByParentId(parentId);
    }

    @Override
    public void add(AgrochemicalCategories category) {
        agrochemicalCategoriesMapper.add(category);
    }

    @Override
    public void update(AgrochemicalCategories category) {
        agrochemicalCategoriesMapper.update(category);
    }

    @Override
    public void deleteById(Integer id) {
        agrochemicalCategoriesMapper.deleteById(id);
    }
}