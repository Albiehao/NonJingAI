package com.example.cropmanagementsystem.mapper;

import com.example.cropmanagementsystem.pojo.Agrochemicals;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface AgrochemicalsMapper {

    /**
     * 插入商品
     */
    @Insert("insert into crop_agrochemicals(category_id, product_code, product_name, brand, " +
            "monthly_sales, price, registration_no, formulation, content_spec, main_image, " +
            "description, use_crops, usage_method, precautions, purchase_links, created_at, updated_at) " +
            "values(#{categoryId}, #{productCode}, #{productName}, #{brand}, " +
            "#{monthlySales}, #{price}, #{registrationNo}, #{formulation}, #{contentSpec}, #{mainImage}, " +
            "#{description}, #{useCrops}, #{usageMethod}, #{precautions}, #{purchaseLinks}, NOW(), NOW())")
    void add(Agrochemicals crop_agrochemicals);

    /**
     * 修改商品
     */
    @Update("update crop_agrochemicals set category_id=#{categoryId}, product_code=#{productCode}, " +
            "product_name=#{productName}, brand=#{brand}, monthly_sales=#{monthlySales}, " +
            "price=#{price}, registration_no=#{registrationNo}, formulation=#{formulation}, " +
            "content_spec=#{contentSpec}, main_image=#{mainImage}, description=#{description}, " +
            "use_crops=#{useCrops}, usage_method=#{usageMethod}, precautions=#{precautions}, " +
            "purchase_links=#{purchaseLinks}, updated_at=NOW() where id=#{id} and deleted_at is null")
    void update(Agrochemicals crop_agrochemicals);

    /**
     * 软删除商品
     */
    @Update("update crop_agrochemicals set deleted_at = NOW() where id = #{id} and deleted_at is null")
    void deleteById(Long id);

    /**
     * 根据ID获取商品（只查未删除）
     */
    @Select("select * from crop_agrochemicals where id = #{id} and deleted_at is null")
    Agrochemicals getById(Long id);

    /**
     * 获取所有商品（只查未删除）
     */
    @Select("select * from crop_agrochemicals where deleted_at is null order by created_at desc")
    List<Agrochemicals> listAll();

    /**
     * 根据分类ID获取商品列表
     */
    @Select("select * from crop_agrochemicals where category_id = #{categoryId} and deleted_at is null order by created_at desc")
    List<Agrochemicals> listByCategoryId(Integer categoryId);

    /**
     * 搜索商品（根据商品名或品牌模糊查询）
     */
    @Select("select * from crop_agrochemicals where (product_name like concat('%', #{keyword}, '%') " +
            "or brand like concat('%', #{keyword}, '%')) and deleted_at is null order by created_at desc")
    List<Agrochemicals> search(String keyword);

    /**
     * 恢复删除
     */
    @Update("update crop_agrochemicals set deleted_at = null where id = #{id}")
    void restoreById(Long id);

}