package com.example.cropmanagementsystem.service;


import com.example.cropmanagementsystem.pojo.Users;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface UserService {
    void register(String username, String password);

    Users login(String username, String password);


    Users selectByUsername(String username);

    void updateUser(Integer id, String username, String phoneNumber, String avatar);

    void deleteUser(Integer id);

    Users getUserById(Integer id);

    List<Users> getAll();
}
