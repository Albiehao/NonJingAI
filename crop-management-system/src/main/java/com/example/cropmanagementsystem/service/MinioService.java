package com.example.cropmanagementsystem.service;

import io.minio.BucketExistsArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.SetBucketPolicyArgs;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.util.UUID;

@Service
public class MinioService {

    @Value("${minio.endpoint:http://minio:9000}")
    private String endpoint;

    @Value("${minio.access-key:minioadmin}")
    private String accessKey;

    @Value("${minio.secret-key:minioadmin}")
    private String secretKey;

    @Value("${minio.avatar-bucket:avatar}")
    private String avatarBucket;

    @Value("${minio.public-endpoint:http://localhost:9000}")
    private String publicEndpoint;

    private MinioClient minioClient;

    @PostConstruct
    public void init() {
        minioClient = MinioClient.builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
        ensureBucketExists(avatarBucket);
    }

    private void ensureBucketExists(String bucket) {
        try {
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucket).build());
            if (!exists) {
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucket).build());
                // 设置为公开读取
                String policy = "{"
                        + "\"Version\":\"2012-10-17\","
                        + "\"Statement\":[{"
                        + "  \"Effect\":\"Allow\","
                        + "  \"Principal\":{\"AWS\":[\"*\"]},"
                        + "  \"Action\":[\"s3:GetObject\"],"
                        + "  \"Resource\":[\"arn:aws:s3:::" + bucket + "/*\"]"
                        + "}]"
                        + "}";
                minioClient.setBucketPolicy(
                        SetBucketPolicyArgs.builder().bucket(bucket).config(policy).build());
            }
        } catch (Exception e) {
            throw new RuntimeException("MinIO bucket init failed: " + bucket, e);
        }
    }

    /**
     * 上传头像到 MinIO
     */
    public String uploadAvatar(MultipartFile file) {
        return uploadFile(file, avatarBucket);
    }

    /**
     * 上传文件到指定 Bucket，返回可公开访问的 URL
     */
    public String uploadFile(MultipartFile file, String bucket) {
        try {
            String originalName = file.getOriginalFilename();
            String ext = "";
            if (originalName != null && originalName.contains(".")) {
                ext = originalName.substring(originalName.lastIndexOf("."));
            }
            String objectName = UUID.randomUUID().toString() + ext;

            String contentType = file.getContentType();
            if (contentType == null) {
                contentType = "application/octet-stream";
            }

            ensureBucketExists(bucket);

            try (InputStream in = file.getInputStream()) {
                minioClient.putObject(
                        PutObjectArgs.builder()
                                .bucket(bucket)
                                .object(objectName)
                                .stream(in, file.getSize(), -1)
                                .contentType(contentType)
                                .build()
                );
            }

            return publicEndpoint + "/" + bucket + "/" + objectName;
        } catch (Exception e) {
            throw new RuntimeException("MinIO upload failed", e);
        }
    }
}
