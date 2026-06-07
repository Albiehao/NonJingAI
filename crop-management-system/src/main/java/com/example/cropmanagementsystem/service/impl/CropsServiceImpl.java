package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.mapper.CropsMapper;
import com.example.cropmanagementsystem.pojo.Crops;
import com.example.cropmanagementsystem.service.CropsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CropsServiceImpl implements CropsService {
    @Autowired
    private CropsMapper cropsMapper;
    //添加作物
    @Override
    public void addCrop(String name, String scientificName) {
        cropsMapper.addCrop(name, scientificName);
    }
    //修改作物

    @Override
    public void updateCrop(Integer id, String name, String scientificName) {
        cropsMapper.updateCrop(id, name, scientificName);
    }

    @Override
    public void deleteById(Integer id) {
        cropsMapper.deleteById(id);
    }

    @Override
    public Crops getById(Integer id) {
        return cropsMapper.getById(id);
    }

    @Override
    public List<Crops> getAll() {
        return cropsMapper.listAll();
    }
}
