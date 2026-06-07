package com.example.cropmanagementsystem.pojo;

import lombok.Data;

/**
 * 聊天请求 DTO
 */
@Data
public class ChatRequest {

    /**
     * 用户消息
     */
    private String message;

    /**
     * 用户ID（可选，用于查询用户作物）
     */
    private Integer userId;

}