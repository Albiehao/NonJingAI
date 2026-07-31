package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Crops;
import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.service.CropsService;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/crops")
public class CropsController {
    @Autowired
    private CropsService cropsService;
    //添加作物
    @PostMapping("/add")
    public Result addCrop(String name, String scientificName) {
        cropsService.addCrop(name, scientificName);
        return Result.success("添加成功");
    }
    //修改作物
    @PostMapping("/update/{id}")
    public Result updateCrop(@PathVariable Integer id,
                             @Param("name") String name,
                             @Param("scientificName") String scientificName) {
        cropsService.updateCrop(id, name, scientificName);
        return Result.success("修改成功");
    }

    //软删除作物（只填写deleted_at）
    @PostMapping("/deleteById/{id}")
    // 软删除：不是真删，是更新删除时间
    public Result deleteById(@PathVariable Integer id){
        cropsService.deleteById(id);
        return Result.success("删除成功");
    }
    //获取单个作物
    @PostMapping("/getById/{id}")
    public Result getById(@PathVariable Integer id){
        Crops crop = cropsService.getById(id);
        return Result.success(crop);
    }

    //获取所有作物
    @PostMapping("/getAll")
    public Result getAll(){
        List<Crops> list = cropsService.getAll();
        return Result.success(list);
    }
}
