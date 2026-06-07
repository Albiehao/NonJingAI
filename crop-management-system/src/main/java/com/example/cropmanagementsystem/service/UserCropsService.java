package com.example.cropmanagementsystem.service;

import com.example.cropmanagementsystem.pojo.UserCrops;

import java.util.List;
import java.util.Map;

public interface UserCropsService {

    // 添加关联
    void addAssociation(Integer userId, Integer cropId);

    // 更新关联
    void updateAssociation(Integer id, Integer userId, Integer cropId);

    // 删除关联
    void deleteById(Integer id);

    // 获取用户的农作物列表
    List<Map<String, Object>> getCropsByUserId(Integer userId);

    // 获取农作物的用户列表
    List<Map<String, Object>> getUsersByCropId(Integer cropId);

    // 获取所有关联
    List<UserCrops> getAll();

    // 检查关联是否存在
    boolean checkExists(Integer userId, Integer cropId);

    // 根据ID获取关联
    UserCrops getById(Integer id);
}