package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Agrochemicals;
import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.service.AgrochemicalsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/agrochemicals")
public class AgrochemicalsController {

    @Autowired
    private AgrochemicalsService agrochemicalsService;

    /**
     * 添加商品
     */
    @PostMapping("/add")
    public Result add(@RequestBody Agrochemicals agrochemicals) {
        agrochemicalsService.add(agrochemicals);
        return Result.success("添加成功");
    }

    /**
     * 修改商品
     */
    @PostMapping("/update")
    public Result update(@RequestBody Agrochemicals agrochemicals) {
        agrochemicalsService.update(agrochemicals);
        return Result.success("修改成功");
    }

    /**
     * 软删除商品
     */
    @PostMapping("/deleteById/{id}")
    public Result deleteById(@PathVariable Long id) {
        agrochemicalsService.deleteById(id);
        return Result.success("删除成功");
    }

    /**
     * 根据ID获取商品
     */
    @GetMapping("/getById/{id}")
    public Result getById(@PathVariable Long id) {
        Agrochemicals agrochemical = agrochemicalsService.getById(id);
        return Result.success(agrochemical);
    }

    /**
     * 获取所有商品
     */
    @GetMapping("/getAll")
    public Result getAll() {
        List<Agrochemicals> list = agrochemicalsService.getAll();
        return Result.success(list);
    }

    /**
     * 根据分类ID获取商品列表
     */
    @GetMapping("/getByCategoryId/{categoryId}")
    public Result getByCategoryId(@PathVariable Integer categoryId) {
        List<Agrochemicals> list = agrochemicalsService.getByCategoryId(categoryId);
        return Result.success(list);
    }

    /**
     * 搜索商品（根据商品名或品牌）
     */
    @GetMapping("/search")
    public Result search(@RequestParam String keyword) {
        List<Agrochemicals> list = agrochemicalsService.search(keyword);
        return Result.success(list);
    }

    /**
     * 搜索商品（POST方式，解决中文编码问题）
     */
    @PostMapping("/searchPost")
    public Result searchPost(@RequestParam String keyword) {
        List<Agrochemicals> list = agrochemicalsService.search(keyword);
        return Result.success(list);
    }

}