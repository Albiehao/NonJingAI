package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.mapper.UserCropsMapper;
import com.example.cropmanagementsystem.pojo.UserCrops;
import com.example.cropmanagementsystem.service.UserCropsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class UserCropsServiceImpl implements UserCropsService {

    @Autowired
    private UserCropsMapper userCropsMapper;

    @Override
    public void addAssociation(Integer userId, Integer cropId) {
        userCropsMapper.addAssociation(userId, cropId);
    }

    @Override
    public void updateAssociation(Integer id, Integer userId, Integer cropId) {
        userCropsMapper.updateAssociation(id, userId, cropId);
    }

    @Override
    public void deleteById(Integer id) {
        userCropsMapper.deleteById(id);
    }

    @Override
    public List<Map<String, Object>> getCropsByUserId(Integer userId) {
        return userCropsMapper.getCropsByUserId(userId);
    }

    @Override
    public List<Map<String, Object>> getUsersByCropId(Integer cropId) {
        return userCropsMapper.getUsersByCropId(cropId);
    }

    @Override
    public List<UserCrops> getAll() {
        return userCropsMapper.getAll();
    }

    @Override
    public boolean checkExists(Integer userId, Integer cropId) {
        return userCropsMapper.checkExists(userId, cropId) > 0;
    }

    @Override
    public UserCrops getById(Integer id) {
        return userCropsMapper.getById(id);
    }
}