package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.mapper.AgrochemicalsMapper;
import com.example.cropmanagementsystem.pojo.Agrochemicals;
import com.example.cropmanagementsystem.service.AgrochemicalsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AgrochemicalsServiceImpl implements AgrochemicalsService {

    @Autowired
    private AgrochemicalsMapper agrochemicalsMapper;

    @Override
    public void add(Agrochemicals agrochemicals) {
        agrochemicalsMapper.add(agrochemicals);
    }

    @Override
    public void update(Agrochemicals agrochemicals) {
        agrochemicalsMapper.update(agrochemicals);
    }

    @Override
    public void deleteById(Long id) {
        agrochemicalsMapper.deleteById(id);
    }

    @Override
    public Agrochemicals getById(Long id) {
        return agrochemicalsMapper.getById(id);
    }

    @Override
    public List<Agrochemicals> getAll() {
        return agrochemicalsMapper.listAll();
    }

    @Override
    public List<Agrochemicals> getByCategoryId(Integer categoryId) {
        return agrochemicalsMapper.listByCategoryId(categoryId);
    }

    @Override
    public List<Agrochemicals> search(String keyword) {
        return agrochemicalsMapper.search(keyword);
    }

}