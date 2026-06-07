package com.example.cropmanagementsystem.mapper;

import com.example.cropmanagementsystem.pojo.UserCrops;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserCropsMapper {

    // 添加用户-农作物关联
    @Insert("insert into crop_user_crops(user_id, crop_id, created_at, updated_at) " +
            "values(#{userId}, #{cropId}, NOW(), NOW())")
    void addAssociation(Integer userId, Integer cropId);

    // 更新用户-农作物关联
    @Update("update crop_user_crops set user_id=#{userId}, crop_id=#{cropId}, " +
            "updated_at=NOW() where id=#{id} and deleted_at is null")
    void updateAssociation(Integer id, Integer userId, Integer cropId);

    // 软删除关联
    @Update("update crop_user_crops set deleted_at = NOW() where id = #{id} and deleted_at is null")
    void deleteById(Integer id);

    // 获取用户的所有农作物（关联查询，返回农作物信息和关联id）
    @Select("select uc.id as associationId, uc.user_id as userId, uc.crop_id as cropId, " +
            "uc.updated_at as updatedAt, c.name as cropName, c.scientific_name as scientificName " +
            "from crop_crops c inner join crop_user_crops uc on c.id = uc.crop_id " +
            "where uc.user_id = #{userId} and uc.deleted_at is null and c.deleted_at is null")
    List<java.util.Map<String, Object>> getCropsByUserId(Integer userId);

    // 获取农作物的所有用户（关联查询，返回用户信息）
    @Select("select u.id, u.username, u.phone_number, u.avatar from crop_users u " +
            "inner join crop_user_crops uc on u.id = uc.user_id " +
            "where uc.crop_id = #{cropId} and uc.deleted_at is null")
    List<java.util.Map<String, Object>> getUsersByCropId(Integer cropId);

    // 获取所有关联（未删除）
    @Select("select * from crop_user_crops where deleted_at is null")
    List<UserCrops> getAll();

    // 检查关联是否存在
    @Select("select count(*) from crop_user_crops where user_id = #{userId} and crop_id = #{cropId} and deleted_at is null")
    int checkExists(Integer userId, Integer cropId);

    // 根据ID获取单条关联
    @Select("select * from crop_user_crops where id = #{id} and deleted_at is null")
    UserCrops getById(Integer id);

}