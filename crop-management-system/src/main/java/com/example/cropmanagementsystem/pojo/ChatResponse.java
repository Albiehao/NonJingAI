package com.example.cropmanagementsystem.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 聊天响应 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatResponse {

    /**
     * AI 回复文本
     */
    private String reply;

    /**
     * 推荐产品列表
     */
    private List<ProductRecommendation> recommendations;

}