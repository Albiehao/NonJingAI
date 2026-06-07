package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.service.MinioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/file")
public class FileUploadController {

    @Autowired
    private MinioService minioService;

    /**
     * 通用文件上传，返回 MinIO 公开访问 URL
     */
    @PostMapping("/upload")
    public Result upload(@RequestParam("file") MultipartFile file,
                         @RequestParam(value = "bucket", defaultValue = "crop-images") String bucket) {
        if (file.isEmpty()) {
            return Result.error("文件不能为空");
        }
        try {
            String url = minioService.uploadFile(file, bucket);
            return Result.success(url);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("上传失败：" + e.getMessage());
        }
    }
}
