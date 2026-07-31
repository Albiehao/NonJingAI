package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.AgrochemicalCategories;
import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.service.AgrochemicalCategoriesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/categories")
public class AgrochemicalCategoriesController {

    @Autowired
    private AgrochemicalCategoriesService agrochemicalCategoriesService;

    /**
     * 获取所有分类
     */
    @GetMapping("/getAll")
    public Result getAll() {
        List<AgrochemicalCategories> list = agrochemicalCategoriesService.getAll();
        return Result.success(list);
    }

    /**
     * 根据ID获取分类
     */
    @GetMapping("/getById/{id}")
    public Result getById(@PathVariable Integer id) {
        AgrochemicalCategories category = agrochemicalCategoriesService.getById(id);
        return Result.success(category);
    }

    /**
     * 获取顶级分类（parent_id为NULL）
     */
    @GetMapping("/getTopCategories")
    public Result getTopCategories() {
        List<AgrochemicalCategories> list = agrochemicalCategoriesService.getTopCategories();
        return Result.success(list);
    }

    /**
     * 根据父分类ID获取子分类
     */
    @GetMapping("/getByParentId/{parentId}")
    public Result getByParentId(@PathVariable Long parentId) {
        List<AgrochemicalCategories> list = agrochemicalCategoriesService.getByParentId(parentId);
        return Result.success(list);
    }

    @PostMapping("/add")
    public Result add(AgrochemicalCategories category) {
        agrochemicalCategoriesService.add(category);
        return Result.success("添加成功");
    }

    @PostMapping("/update/{id}")
    public Result update(@PathVariable Integer id, AgrochemicalCategories category) {
        category.setId(id);
        agrochemicalCategoriesService.update(category);
        return Result.success("修改成功");
    }

    @PostMapping("/deleteById/{id}")
    public Result deleteById(@PathVariable Integer id) {
        agrochemicalCategoriesService.deleteById(id);
        return Result.success("删除成功");
    }
}