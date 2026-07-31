package com.example.cropmanagementsystem.exception;

import com.example.cropmanagementsystem.pojo.Result;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;


@RestControllerAdvice // 表示该类是异常处理器
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class) // 表示该方法可以处理所有类型异常
    public Result handleException(Exception e){
        e.printStackTrace();
        return Result.error(StringUtils.hasLength(e.getMessage()) ? e.getMessage() : "操作失败"); // 返回错误信息
    }
}
