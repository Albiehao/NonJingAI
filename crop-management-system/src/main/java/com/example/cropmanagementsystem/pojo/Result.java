package com.example.cropmanagementsystem.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result<T> {
//    全局返回值
    private int code;//状态码
    private String message;//提示信息
    private T data;//响应数据
    //快速返回操作成功响应结果(带响应数据)
    public static <T> Result<T> success(T data) {
        return new Result<>(0, "操作成功", data);
    }

    // 成功：自定义提示 + 数据
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(0, message, data);
    }

    // ====================== 标准失败返回 ======================
    public static <T> Result<T> error(String message) {
        return new Result<>(1, message, null);
    }
}
