package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.pojo.UserCrops;
import com.example.cropmanagementsystem.service.UserCropsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/userCrops")
public class UserCropsController {

    @Autowired
    private UserCropsService userCropsService;

    // 添加用户-农作物关联
    @PostMapping("/add")
    public Result addAssociation(Integer userId, Integer cropId) {
        // 检查关联是否已存在
        if (userCropsService.checkExists(userId, cropId)) {
            return Result.error("该用户与农作物的关联已存在");
        }
        userCropsService.addAssociation(userId, cropId);
        return Result.success("添加关联成功");
    }

    // 更新用户-农作物关联
    @PostMapping("/update/{id}")
    public Result updateAssociation(@PathVariable Integer id, Integer userId, Integer cropId) {
        // 检查关联是否存在
        UserCrops existing = userCropsService.getById(id);
        if (existing == null) {
            return Result.error("关联不存在或已被删除");
        }
        // 检查新的关联是否已存在（排除当前关联）
        if (userCropsService.checkExists(userId, cropId) &&
            !(existing.getUserId().equals(userId) && existing.getCropId().equals(cropId))) {
            return Result.error("该用户与农作物的关联已存在");
        }
        userCropsService.updateAssociation(id, userId, cropId);
        return Result.success("更新关联成功");
    }

    // 删除用户-农作物关联（软删除）
    @PostMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        UserCrops existing = userCropsService.getById(id);
        if (existing == null) {
            return Result.error("关联不存在或已被删除");
        }
        userCropsService.deleteById(id);
        return Result.success("删除关联成功");
    }

    // 获取用户的农作物列表
    @PostMapping("/getByUser/{userId}")
    public Result getCropsByUserId(@PathVariable Integer userId) {
        List<Map<String, Object>> crops = userCropsService.getCropsByUserId(userId);
        return Result.success(crops);
    }

    // 获取农作物的用户列表
    @PostMapping("/getByCrop/{cropId}")
    public Result getUsersByCropId(@PathVariable Integer cropId) {
        List<Map<String, Object>> users = userCropsService.getUsersByCropId(cropId);
        return Result.success(users);
    }

    // 获取所有关联
    @PostMapping("/getAll")
    public Result getAll() {
        List<UserCrops> list = userCropsService.getAll();
        return Result.success(list);
    }
}