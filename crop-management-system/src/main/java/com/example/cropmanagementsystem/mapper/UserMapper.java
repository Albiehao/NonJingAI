package com.example.cropmanagementsystem.mapper;

import com.example.cropmanagementsystem.pojo.Users;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserMapper {
    @Insert("insert into crop_users (username, password) values (#{username}, #{password})")
    void register(String username, String password); // 注册用户
    //登录
    @Select("select * from crop_users where username = #{username}")
    Users login(@Param("username") String username); // 登录用户

    @Select("select * from crop_users where username = #{username}")
    Users selectByUsername(@Param("username") String username);



    //修改 - 只在有新值时才更新对应字段
    @Update("update crop_users set " +
            "username = CASE WHEN #{username, jdbcType=VARCHAR} IS NOT NULL AND #{username, jdbcType=VARCHAR} != '' THEN #{username, jdbcType=VARCHAR} ELSE username END, " +
            "phone_number = CASE WHEN #{phoneNumber, jdbcType=VARCHAR} IS NOT NULL AND #{phoneNumber, jdbcType=VARCHAR} != '' THEN #{phoneNumber, jdbcType=VARCHAR} ELSE phone_number END, " +
            "avatar = CASE WHEN #{avatar, jdbcType=VARCHAR} IS NOT NULL AND #{avatar, jdbcType=VARCHAR} != '' THEN #{avatar, jdbcType=VARCHAR} ELSE avatar END " +
            "where id = #{id}")
    void updateUser(Integer id, String username, String phoneNumber, String avatar);

    //删除
    @Delete("delete from crop_users where id = #{id}")
    void deleteUser(Integer id);
    //单个用户查询
    @Select("select * from crop_users where id = #{id}")
    Users getUserById(Integer id);
    //查询所有用户
    @Select("select * from crop_users")
    List<Users> getAll();
}
