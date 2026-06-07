package com.example.cropmanagementsystem.pojo;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Entity
public class Users {
    @Id
    private Integer id;

    private String username;

    private String phoneNumber;

    private String avatar;

    private String password;

    private String role;

    private LocalDateTime createdAt;
}
