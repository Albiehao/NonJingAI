package com.example.cropmanagementsystem;
import com.example.cropmanagementsystem.util.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class CropManagementSystemApplicationTests {
    @Autowired
    private JwtUtil jwtUtil;

//    测试jwt
    @Test
    void testJwt() {
        // 直接使用注入的jwtUtil，不再new
        String token = jwtUtil.generateToken(5, "ADMIN", "123456");
        System.out.println("生成的Token：" + token);

        // 可选：验证Token有效性
        boolean isValid = jwtUtil.validateToken(token);
        System.out.println("Token是否有效：" + isValid);
    }

}
