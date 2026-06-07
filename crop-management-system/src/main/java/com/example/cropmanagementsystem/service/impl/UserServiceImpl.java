package com.example.cropmanagementsystem.service.impl;

import com.example.cropmanagementsystem.mapper.UserMapper;
import com.example.cropmanagementsystem.pojo.Result;
import com.example.cropmanagementsystem.pojo.Users;
import com.example.cropmanagementsystem.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private PasswordEncoder passwordEncoder;
    @Override
    public void register(String username, String password) {
        String encodedPassword = passwordEncoder.encode(password);
        userMapper.register(username,encodedPassword);
    }

    @Override
    public Users login(String username, String password) {
        Users user = userMapper.login(username);
        if (user == null){
            return null;
        }
        // 密码匹配
        boolean isMatch = passwordEncoder.matches(password, user.getPassword());
        if (isMatch) {
            return user; // 匹配成功，返回用户信息
        }
        return null;
    }

    @Override
    public Users selectByUsername(String username) {
        return userMapper.selectByUsername(username);
    }

    // 修改

    @Override

    public void updateUser(Integer id, String username, String phoneNumber,String avatar) {
        userMapper.updateUser(id, username, phoneNumber, avatar);
    }
    //删除

    @Override
    public void deleteUser(Integer id) {
        userMapper.deleteUser(id);
    }

    @Override
    public Users getUserById(Integer id) {

        return userMapper.getUserById(id);
    }

    @Override
    public List<Users> getAll() {

        return userMapper.getAll();
    }
}
