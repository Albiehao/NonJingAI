package com.example.cropmanagementsystem.mapper;

import com.example.cropmanagementsystem.pojo.Crops;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface CropsMapper {
    // 插入：用函数生成时间
    @Insert("insert into crop_crops(name, scientific_name, created_at, updated_at) " +
            "values(#{name}, #{scientificName}, NOW(), NOW())")
    void addCrop(String name, String scientificName);
    //修改
    @Update("update crop_crops set name=#{name}, scientific_name=#{scientificName}, " +
            "updated_at=NOW() where id=#{id}")
    void updateCrop(Integer id, String name, String scientificName);



    //软删除
    @Update("update crop_crops set deleted_at = NOW() where id = #{id} and deleted_at is null")
    void deleteById(Integer id);

    // 查询：只查未删除的数据（核心！）
    @Select("select * from crop_crops where id = #{id} and deleted_at is null")
    Crops getById(Integer id);

    // 查询列表：只查未删除的数据
    @Select("select * from crop_crops where deleted_at is null")
    List<Crops> listAll();

    // 恢复删除：把deleted_at改回NULL
    @Update("update crop_crops set deleted_at = null where id = #{id}")
    void restoreById(Integer id);


}
