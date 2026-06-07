package com.example.cropmanagementsystem.tools;

import com.example.cropmanagementsystem.pojo.Crops;
import com.example.cropmanagementsystem.service.CropsService;
import dev.langchain4j.agent.tool.Tool;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * 作物查询工具
 * 提供给 AI Agent 使用
 */
@Component
public class CropTools {

    @Autowired
    private CropsService cropsService;

    /**
     * 获取所有作物（LangChain4j Tool 必须有参数）
     */
    @Tool("获取系统中所有农作物列表，参数可以是任意字符串")
    public String getAllCrops(String query) {
        List<Crops> crops = cropsService.getAll();
        if (crops == null || crops.isEmpty()) {
            return "暂无作物数据";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("系统中共有 ").append(crops.size()).append(" 种作物:\n");
        for (Crops c : crops) {
            sb.append("- ID: ").append(c.getId())
              .append(", 名称: ").append(c.getName())
              .append(", 学名: ").append(c.getScientificName())
              .append("\n");
        }
        return sb.toString();
    }

    /**
     * 根据名称查询作物
     */
    @Tool("根据作物名称查询作物信息，如水稻、小麦等")
    public String getCropByName(String name) {
        List<Crops> crops = cropsService.getAll();
        if (crops == null || crops.isEmpty()) {
            return "暂无作物数据";
        }
        for (Crops c : crops) {
            if (c.getName().equals(name) || c.getName().contains(name)) {
                return "作物信息: ID=" + c.getId() + ", 名称=" + c.getName() + ", 学名=" + c.getScientificName();
            }
        }
        return "未找到该作物: " + name;
    }

}