package com.example.cropmanagementsystem.tools;

import com.example.cropmanagementsystem.pojo.Agrochemicals;
import com.example.cropmanagementsystem.service.AgrochemicalsService;
import dev.langchain4j.agent.tool.Tool;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 农资产品查询工具
 * 提供给 AI Agent 使用
 */
@Component
public class AgrochemicalTools {

    @Autowired
    private AgrochemicalsService agrochemicalsService;

    /**
     * 搜索农资产品
     */
    @Tool("搜索农资产品，根据关键词搜索商品名或品牌")
    public String searchProducts(String keyword) {
        List<Agrochemicals> products = agrochemicalsService.search(keyword);
        return formatProducts(products);
    }

    /**
     * 根据分类ID获取产品
     */
    @Tool("根据分类ID获取农资产品列表，分类ID: 1-杀菌剂, 2-杀虫剂, 3-除草剂, 4-植物生长调节剂, 5-肥料")
    public String getProductsByCategory(Integer categoryId) {
        List<Agrochemicals> products = agrochemicalsService.getByCategoryId(categoryId);
        return formatProducts(products);
    }

    /**
     * 根据适用作物查询产品
     */
    @Tool("根据作物名称查询适用的农资产品，例如输入'水稻'返回适用于水稻的农药肥料")
    public String getProductsByCrop(String cropName) {
        List<Agrochemicals> allProducts = agrochemicalsService.getAll();
        // 过滤适用作物包含指定名称的产品
        List<Agrochemicals> filtered = allProducts.stream()
                .filter(p -> p.getUseCrops() != null && p.getUseCrops().contains(cropName))
                .collect(Collectors.toList());
        return formatProducts(filtered);
    }

    /**
     * 获取产品详情
     */
    @Tool("根据产品ID获取农资产品详细信息")
    public String getProductById(Long productId) {
        Agrochemicals product = agrochemicalsService.getById(productId);
        if (product == null) {
            return "未找到该产品";
        }
        return formatProductDetail(product);
    }

    /**
     * 联网搜索
     */
    @Tool("联网搜索")
    public String searchOnline(String keyword) {
        // 使用联网搜索功能
        return "联网搜索功能已启用，请稍等...";
    }


    /**
     * 格式化产品列表为字符串
     */
    private String formatProducts(List<Agrochemicals> products) {
        if (products == null || products.isEmpty()) {
            return "未找到相关产品";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("找到 ").append(products.size()).append(" 个产品:\n");
        for (Agrochemicals p : products) {
            sb.append("- ID: ").append(p.getId())
              .append(", 名称: ").append(p.getProductName())
              .append(", 品牌: ").append(p.getBrand())
              .append(", 价格: ").append(p.getPrice())
              .append(", 适用作物: ").append(p.getUseCrops())
              .append("\n");
        }
        return sb.toString();
    }

    /**
     * 格式化单个产品详情
     */
    private String formatProductDetail(Agrochemicals p) {
        StringBuilder sb = new StringBuilder();
        sb.append("产品详情:\n");
        sb.append("ID: ").append(p.getId()).append("\n");
        sb.append("名称: ").append(p.getProductName()).append("\n");
        sb.append("品牌: ").append(p.getBrand()).append("\n");
        sb.append("价格: ").append(p.getPrice()).append("\n");
        sb.append("剂型: ").append(p.getFormulation()).append("\n");
        sb.append("适用作物: ").append(p.getUseCrops()).append("\n");
        sb.append("用法: ").append(p.getUsageMethod()).append("\n");
        sb.append("注意事项: ").append(p.getPrecautions()).append("\n");
        sb.append("跳转链接: /products/").append(p.getId()).append("\n");
        return sb.toString();
    }


}