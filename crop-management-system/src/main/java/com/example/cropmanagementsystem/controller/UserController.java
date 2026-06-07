package com.example.cropmanagementsystem.controller;

import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.pojo.Users;
import com.example.cropmanagementsystem.service.MinioService;
import com.example.cropmanagementsystem.service.UserService;
import com.example.cropmanagementsystem.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/user")
public class UserController {
    @Autowired
    private UserService userService;
    @Autowired
    private JwtUtil jwtUtil;
    @Autowired
    private PasswordEncoder passwordEncoder;
    @Autowired
    private MinioService minioService;
    //注册
    @PostMapping("/register")
    public Result register(String username, String password) {
//        用户不能重名
        Users existUser = userService.selectByUsername(username);
        if (existUser != null) {
            return Result.error("用户名已存在");
        }

        userService.register(username, password);
        return Result.success("注册成功");
    }
    //登录
    @PostMapping("/login")
    public Result login(String username,String password) {
        Users user = userService.login(username, password);
        if (user == null) {
            return Result.error("用户名或密码错误");
        }

        // 登录成功 → 生成JWT令牌（给前端用）
        String token = jwtUtil.generateToken(user.getId(), username, user.getRole());

        // 返回用户信息（包含角色）
        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("id", user.getId());
        data.put("username", user.getUsername());
        data.put("role", user.getRole());
        data.put("avatar", user.getAvatar());

        return Result.success("登录成功", data);
    }

    //修改
    // 修改用户信息 + 上传头像图片
    @PostMapping(value = "/update/{id}", consumes = "multipart/form-data")
    public Result update(
            @PathVariable Integer id,
            @RequestParam(value = "username", required = false) String username,
            @RequestParam(value = "phoneNumber", required = false) String phoneNumber,
            @RequestParam(value = "avatar", required = false) MultipartFile avatar // 接收图片
    ) {
        System.out.println("收到更新请求，id=" + id + ", username=" + username + ", phoneNumber=" + phoneNumber);
        System.out.println("avatar文件是否为空：" + (avatar == null ? "是" : "否，大小：" + avatar.getSize() + "，名称：" + avatar.getOriginalFilename()));

        String avatarUrl = null;
        // 如果上传了图片，就上传到 MinIO
        if (avatar != null && !avatar.isEmpty()) {
            try {
                avatarUrl = minioService.uploadAvatar(avatar);
                System.out.println("MinIO上传成功：" + avatarUrl);
            } catch (Exception e) {
                e.printStackTrace();
                return Result.error("头像上传失败：" + e.getMessage());
            }
        }

        // 执行更新（头像地址存入数据库）
        userService.updateUser(id, username, phoneNumber, avatarUrl);
        System.out.println("用户更新完成，avatarUrl=" + avatarUrl);

        // 返回更新后的完整用户信息
        Users updatedUser = userService.getUserById(id);
        Map<String, Object> data = new HashMap<>();
        data.put("avatar", updatedUser.getAvatar());
        data.put("username", updatedUser.getUsername());
        data.put("phoneNumber", updatedUser.getPhoneNumber());
        return Result.success("修改成功", data);
    }
    //删除
    @PostMapping("/delete/{id}")
    public Result delete(@PathVariable Integer id) {
        userService.deleteUser(id);
        return Result.success("删除成功");
    }

    //获取单个用户信息
    @PostMapping("/get/{id}")
    public Result get(@PathVariable Integer id) {
        Users user = userService.getUserById(id);
        return Result.success(user);
    }
    //获取所有用户信息
    @PostMapping("/getAll")
    public Result getAll() {
        List<Users> list = userService.getAll();
        return Result.success(list);
    }
}
