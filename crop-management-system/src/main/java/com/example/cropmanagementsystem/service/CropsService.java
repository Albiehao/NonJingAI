package com.example.cropmanagementsystem.service;

import com.example.cropmanagementsystem.pojo.Crops;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface CropsService {
    void addCrop(String name, String scientificName);

    void updateCrop(Integer id, String name, String scientificName);

    void deleteById(Integer id);

    Crops getById(Integer id);

    List<Crops> getAll();
}
